import pathlib

import click
import pkg_resources

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.schema import ModelSchema, deepmerge

import logging

from oarepo_model_builder.utils.verbose import log


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
@click.argument('model_filename')
def run(output_directory, package, sets, configs, model_filename, verbosity):
    """
    Compiles an oarepo model file given in MODEL_FILENAME into an Invenio repository model.
    """

    # set the logging level, it will be warning - 1 (that is, 29) if not verbose,
    # so that warnings only will be emitted. With each verbosity level
    # it will decrease
    logging.basicConfig(
        level=logging.WARNING - verbosity,
        format=''
    )

    log.enter(1, 'Processing model %s into output directory %s',
              model_filename, output_directory)

    output_classes = load_entry_points_list('oarepo_model_builder.ouptuts')
    builder_classes = load_entry_points_list('oarepo_model_builder.builders')
    preprocess_classes = load_entry_points_list('oarepo_model_builder.property_preprocessors')
    model_preprocessor_classes = load_entry_points_list('oarepo_model_builder.model_preprocessors')
    loaders = load_entry_points_dict('oarepo_model_builder.loaders')
    safe_loaders = {k: v for k, v in loaders.items() if getattr(v, 'safe', False)}

    schema = ModelSchema(model_filename, loaders=safe_loaders)
    for config in configs:
        load_config(schema, config, loaders)

    for s in sets:
        k, v = s.split('=', 1)
        schema.schema[k] = v

    if package:
        schema.schema['package'] = package

    builder = ModelBuilder(
        output_builders=builder_classes,
        outputs=output_classes,
        output_preprocessors=preprocess_classes,
        model_preprocessors=model_preprocessor_classes
    )

    builder.build(schema, output_directory)

    log.leave('Done')


def load_entry_points_dict(name):
    return {ep.name: ep.load() for ep in pkg_resources.iter_entry_points(group=name)}


def load_entry_points_list(name):
    ret = [(ep.name, ep.load()) for ep in pkg_resources.iter_entry_points(group=name)]
    ret.sort()
    return [x[1] for x in ret]


def load_config(schema, config, loaders):
    old_loaders = schema.loaders
    schema.loaders = loaders
    try:
        loaded_file = schema._load(config)
        schema.schema = deepmerge(loaded_file, schema.schema, [])
    finally:
        schema.loaders = old_loaders


if __name__ == '__main__':
    run()
