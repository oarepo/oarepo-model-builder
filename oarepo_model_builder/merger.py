import json
import shutil
import sys
from functools import partial
from pathlib import Path

import click
import json5
import libcst as cst
import yaml

from oarepo_model_builder.utils.cst import PythonContext, merge
from oarepo_model_builder.utils.deepmerge import deepmerge


@click.command()
@click.argument("source", type=click.Path(file_okay=True, dir_okay=True, exists=True))
@click.argument(
    "destination", type=click.Path(file_okay=True, dir_okay=True, exists=False)
)
@click.option(
    "--result",
    type=click.Path(file_okay=True, dir_okay=True),
    help="Do not overwrite destination, write to this path instead",
)
@click.option(
    "--destination-first/--source-first",
    help="Take destination first and merge source only if it is not in destination. Normally merges destination into source and replaces destination with the result",
)
@click.option(
    "--overwrite/--no-overwrite",
    help="Do not perform merging but overwrite destination files with source files",
)
def merger(source, destination, result, destination_first, overwrite):
    source = Path(source)
    destination = Path(destination)

    if source.is_file():
        if destination.exists() and not destination.is_file():
            click.echo(
                "If source is a file, destination must be a file as well", err=True
            )
            sys.exit(1)
        merge_file(
            source, destination, result or destination, destination_first, overwrite
        )
    else:
        for fn in source.glob("**/*"):
            if not fn.is_file():
                continue
            relative_fn = fn.relative_to(source)
            merge_file(
                fn,
                destination.joinpath(relative_fn),
                (
                    result.joinpath(relative_fn)
                    if result
                    else destination.joinpath(relative_fn)
                ),
                destination_first,
                overwrite,
            )


def merge_file(
    source: Path,
    destination: Path,
    result: Path,
    destination_first: bool,
    overwrite: bool,
):
    source_suffix = source.suffix[1:]
    destination_suffix = destination.suffix[1:]
    if source_suffix != destination_suffix:
        raise AttributeError(
            f"Suffixes of source and destination files must match, have {source}, {destination}"
        )
    result.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists() or overwrite:
        if source.is_file():
            shutil.copy(source, result)
        else:
            shutil.copytree(source, result, dirs_exist_ok=True)
        return
    if source_suffix == "yaml":
        merge_json(
            source,
            destination,
            result,
            destination_first,
            yaml.safe_load,
            yaml.safe_dump,
        )
    elif source_suffix == "json":
        merge_json(
            source,
            destination,
            result,
            destination_first,
            json.load,
            partial(json.dump, indent=4, ensure_ascii=False),
        )
    elif source_suffix == "json5":
        merge_json(
            source,
            destination,
            result,
            destination_first,
            json5.load,
            partial(json5.dump, indent=4, ensure_ascii=False),
        )
    elif source_suffix == "py":
        merge_python(source, destination, result, destination_first)
    else:
        raise NotImplementedError(
            f"Merging file type {source_suffix} (file {source}) is not implemented yet"
        )


def merge_json(
    source, destination, result: Path, destination_first, load_func, dump_func
):
    with open(source) as f:
        source_data = load_func(f)
    with open(destination) as f:
        destination_data = load_func(f)
    if destination_first:
        deepmerge(destination_data, source_data)
    else:
        deepmerge(source_data, destination_data)
        destination_data = source_data
    with open(result, "w") as f:
        dump_func(destination_data, f)


def merge_python(source: Path, destination: Path, result, destination_first: bool):
    source_cst = cst.parse_module(source.read_text())
    destination_cst = cst.parse_module(destination.read_text())
    if destination_first:
        result_cst = merge(
            PythonContext(source_cst),
            destination_cst,
            source_cst,
        )
    else:
        result_cst = merge(
            PythonContext(destination_cst),
            source_cst,
            destination_cst,
        )
    # write the merged files out
    with open(result, "w") as f:
        f.write(result_cst.code)

    # code style
    import subprocess

    import isort

    config = isort.settings.Config(verbose=False, quiet=True)
    isort.file(result, config=config)
    subprocess.call(["black", "-q", "--preview", str(result)])


if __name__ == "__main__":
    merger()
