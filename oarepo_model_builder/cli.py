import datetime
import json
import logging
import os
import sys
import traceback
from pathlib import Path

import click
import yaml

from oarepo_model_builder.entrypoints import (
    create_builder_from_entrypoints,
    load_entry_points_dict,
    load_model,
)
from oarepo_model_builder.utils.verbose import log


@click.command()
@click.option(
    "--output-directory",
    help="Output directory where the generated files will be placed. "
    'Defaults to "."',
)
@click.option(
    "--package",
    help="Package into which the model is generated. "
    "If not passed, the name of the output directory, "
    "converted into python package name, is used.",
)
@click.option(
    "--set",
    "sets",
    help="Overwrite option in the model file. Example: --set name=value",
    multiple=True,
)
@click.option(
    "-v",
    "verbosity",
    help="Increase the verbosity. This option can be used multiple times.",
    count=True,
)
@click.option(
    "--save-model",
    "save_model",
    help="Save resolved model into this file.",
)
@click.option(
    "--config",
    "configs",
    help="Load a config file and replace parts of the model with it. "
    "The config file can be a json, yaml or a python file. "
    "If it is a python file, it is evaluated with the current "
    'model stored in the "oarepo_model" global variable.',
    multiple=True,
)
@click.option(
    "--include",
    "includes",
    help="A pair of symbolic-name=path-to-the-file. "
    'If the schema contains "use: <symbolic-name>" or "extend: <symbolic-name>", '
    "it will be converted into the file path and imported.",
    multiple=True,
)
@click.option(
    "--isort/--skip-isort", default=True, help="Call isort on generated sources"
)
@click.option(
    "--black/--skip-black", default=True, help="Call black on generated sources"
)
@click.option(
    "--autoflake/--skip-autoflake",
    default=True,
    help="Call autoflake on generated sources",
)
@click.option(
    "--overwrite",
    type=bool,
    default=False,
    help="Do not merge with content in already existing files, overwrite them",
)
@click.option(
    "--profile",
    help="Run the builder with this profile",
    default=[],
    multiple=True,
)
@click.argument("model_filename", type=click.Path(exists=True), required=True)
@click.argument(
    "included_models", nargs=-1, type=click.Path(exists=True), required=False
)
def run(
    output_directory,  # NOSONAR
    package,
    sets,
    configs,
    model_filename,
    included_models,
    verbosity,
    isort,
    black,
    autoflake,
    save_model,
    overwrite,
    profile,
    includes,
):
    """
    Compiles an oarepo model file given in MODEL_FILENAME into an Invenio repository model.
    """
    try:
        run_internal(
            output_directory,
            model_filename,
            included_models,
            package,
            configs,
            sets,
            black,
            isort,
            autoflake,
            verbosity,
            save_model,
            overwrite,
            profile,
            includes,
        )
    except Exception as e:
        if verbosity >= 2:
            print(e, file=sys.stderr)
            traceback.print_exc()
        elif verbosity >= 1:
            print(e, file=sys.stderr)
            traceback.print_exc(limit=-5)
        else:
            print(e, file=sys.stderr)
        sys.exit(1)


def run_internal(
    output_directory,  # NOSONAR
    model_filename,
    included_models,
    package,
    configs,
    sets,
    black,
    isort,
    autoflake,
    verbosity,
    save_model,
    overwrite,
    profiles,
    includes,
):
    # extend system's search path to add script's path in front (so that scripts called from the compiler are taken
    # from the correct virtual environ)
    os.environ["PATH"] = (
        str(Path(sys.argv[0]).parent.absolute())
        + os.pathsep
        + os.environ.get("PATH", "")
    )
    if not output_directory:
        output_directory = os.getcwd()

    if not package:
        package = Path(model_filename).name.split(".")[0]

    # set the logging level, it will be warning - 1 (that is, 29) if not verbose,
    # so that warnings only will be emitted. With each verbosity level
    # it will decrease
    logging.basicConfig(level=logging.INFO - verbosity, format="")

    # create the output directory and set the installation log file
    Path(output_directory).mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(Path(output_directory) / "installation.log", "a")
    handler.setLevel(logging.INFO)
    logging.root.addHandler(handler)

    # log intro
    log.enter(
        0,
        "\n\n%s\n\nProcessing model(s) %s into output directory %s",
        datetime.datetime.now(),
        [model_filename, *included_models],
        output_directory,
    )

    includes = {
        x.split("=", maxsplit=1)[0]: x.split("=", maxsplit=1)[1] for x in includes
    }

    # load model (and resolve includes) and optionally save it before the processing (for debugging)
    model = load_model(
        model_filename,
        configs,
        black,
        isort,
        autoflake,
        sets,
        merged_models=included_models,
        extra_included=includes,
    )
    if save_model:
        with open(save_model, "w") as f:
            yaml.dump(json.loads(json.dumps(model.schema)), f)
    if not profiles:
        profiles = model.schema.get("profiles", ["record"])

    # for each profile on the command line, render it
    profiles_to_render = [y.strip() for x in profiles for y in x.split(",")]
    for profile in profiles_to_render:
        # load the builder
        builder = create_builder_from_entrypoints(profile=profile, overwrite=overwrite)

        # load profile handler
        try:
            profile_handler = load_entry_points_dict("oarepo_model_builder.profiles")[
                profile
            ]()
        except KeyError:
            raise AttributeError(f"No profile handler for {profile} registered")

        # and call it
        profile_handler.build(
            model,
            profile,
            profile_handler.default_model_path,
            output_directory,
            builder,
        )
    log.leave("Done")
    print(f"Log saved to {Path(output_directory) / 'installation.log'}")


if __name__ == "__main__":
    run()
