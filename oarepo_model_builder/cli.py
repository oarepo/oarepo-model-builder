import datetime
import logging
import os
import sys
from pathlib import Path

import click

from oarepo_model_builder.entrypoints import load_entry_points_dict, create_builder_from_entrypoints
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.utils.deepmerge import deepmerge
from oarepo_model_builder.utils.verbose import log

from .utils.hyphen_munch import HyphenMunch


@click.command()
@click.option('--output-directory',
              help='Output directory where the generated files will be placed. '
                   'Defaults to "."')
@click.option('--package',
              help='Package into which the model is generated. '
                   'If not passed, the name of the current directory, '
                   'converted into python package name, is used.')
@click.option('--set', 'sets',
              help='Overwrite option in the model file. Example '
                   '--set name=value',
              multiple=True)
@click.option('-v', 'verbosity',
              help='Increase the verbosity. This option can be used multiple times.',
              count=True)
@click.option('--config', 'configs',
              help='Load a config file and replace parts of the model with it. '
                   'The config file can be a json, yaml or a python file. '
                   'If it is a python file, it is evaluated with the current '
                   'model stored in the "oarepo_model" global variable and '
                   'after the evaluation all globals are set on the model.',
              multiple=True)
@click.option('--isort/--skip-isort', default=True, help='Call isort on generated sources')
@click.option('--black/--skip-black', default=True, help='Call black on generated sources')
@click.argument('model_filename')
def run(output_directory, package, sets, configs, model_filename, verbosity, isort, black):
    """
    Compiles an oarepo model file given in MODEL_FILENAME into an Invenio repository model.
    """

    # extend system's search path to add script's path in front (so that scripts called from the compiler are taken
    # from the correct virtual environ)
    os.environ['PATH'] = str(Path(sys.argv[0]).parent.absolute()) + os.pathsep + os.environ.get('PATH', '')

    # set the logging level, it will be warning - 1 (that is, 29) if not verbose,
    # so that warnings only will be emitted. With each verbosity level
    # it will decrease
    logging.basicConfig(
        level=logging.INFO - verbosity,
        format=''
    )

    handler = logging.FileHandler(Path(output_directory) / 'installation.log', 'a')
    handler.setLevel(logging.INFO)
    logging.root.addHandler(handler)

    log.enter(0, '\n\n%s\n\nProcessing model %s into output directory %s',
              datetime.datetime.now(), model_filename, output_directory)

    builder = create_builder_from_entrypoints()
    loaders = load_entry_points_dict('oarepo_model_builder.loaders')
    safe_loaders = {k: v for k, v in loaders.items() if getattr(v, 'safe', False)}

    schema = ModelSchema(model_filename, loaders=safe_loaders)
    for config in configs:
        load_config(schema, config, loaders)

    for s in sets:
        k, v = s.split('=', 1)
        schema.schema[k] = v

    check_plugin_packages(schema.settings)

    if package:
        schema.settings['package'] = package

    if 'python' not in schema.settings:
        schema.settings.python = HyphenMunch()
    schema.settings.python.use_isort = isort
    schema.settings.python.use_black = black

    builder.build(schema, output_directory)

    log.leave('Done')

    print(f"Log saved to {Path(output_directory) / 'installation.log'}")


def load_config(schema, config, loaders):
    old_loaders = schema.loaders
    schema.loaders = loaders
    try:
        loaded_file = schema._load(config)
        schema.merge(loaded_file)
    finally:
        schema.loaders = old_loaders


def check_plugin_packages(settings):
    try:
        required_packages = settings.plugins.packages
    except AttributeError:
        return
    import pkg_resources, subprocess
    known_packages = set(d.project_name for d in pkg_resources.working_set)
    unknown_packages = [rp for rp in required_packages if rp not in known_packages]
    if unknown_packages:
        if input(f'Required packages {", ".join(unknown_packages)} are missing. '
                 f'Should I install them for you via pip install? (y/n) ') == 'y':
            if subprocess.call([
                'pip', 'install', *unknown_packages
            ]):
                sys.exit(1)
            print("Installed required packages, please run this command again")
        sys.exit(1)


if __name__ == '__main__':
    run()
