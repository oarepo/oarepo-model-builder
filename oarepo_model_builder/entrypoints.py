import sys
from functools import reduce
from importlib import import_module
from pathlib import Path

import importlib_metadata
import importlib.resources

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.schema import ModelSchema, remove_star_keys
from oarepo_model_builder.utils.hyphen_munch import HyphenMunch


def create_builder_from_entrypoints(**kwargs):
    output_classes = load_entry_points_list("oarepo_model_builder.outputs")
    builder_classes = load_entry_points_list("oarepo_model_builder.builders")
    preprocess_classes = load_entry_points_list(
        "oarepo_model_builder.property_preprocessors"
    )
    model_preprocessor_classes = load_entry_points_list(
        "oarepo_model_builder.model_preprocessors"
    )

    builder_types = [x.TYPE for x in builder_classes]
    output_builder_components = {
        builder_type: load_entry_points_list(
            f"oarepo_model_builder.builder_components.{builder_type}"
        )
        for builder_type in builder_types
    }

    return ModelBuilder(
        output_builders=builder_classes,
        outputs=output_classes,
        property_preprocessors=preprocess_classes,
        model_preprocessors=model_preprocessor_classes,
        output_builder_components=output_builder_components,
        **kwargs,
    )


def load_entry_points_dict(name):
    return {
        ep.name: ep.load()
        for ep in importlib_metadata.entry_points().select(group=name)
    }


def load_entry_points_list(name):
    ret = []
    loaded = {}
    for ep in importlib_metadata.entry_points().select(group=name):
        if ep.name in loaded:
            print(
                f"WARNING: Entry point {ep.name} has already been registered to group {name}. "
                f"Previous value {loaded[ep.name]}, new ignored value {ep.value}"
            )
            continue
        ret.append((ep.name, ep.load()))
        loaded[ep.name] = ep.value
    ret.sort()
    return [x[1] for x in ret]


def load_model_from_entrypoint(ep: importlib_metadata.EntryPoint):
    def load(schema):
        try:
            loaded_schema = ep.load()
        except:
            module = import_module(ep.module)
            split_attr = ep.attr.split(".")
            fn = f"{split_attr[-2]}.{split_attr[-1]}"
            if len(split_attr) > 2:
                fn = reduce(lambda x, y: Path(x) / Path(y), split_attr[:-2]) / fn
            module_path = getattr(module, "__path__", [])
            if module_path:
                full_fn = Path(module_path[0]) / fn
            else:
                full_fn = fn
            content = importlib.resources.open_text(module, fn, encoding="utf-8").read()
            loaded_schema = schema._load(full_fn, content=content)

        remove_star_keys(loaded_schema)
        return loaded_schema

    return load


def load_included_models_from_entry_points():
    ret = {}
    for ep in importlib_metadata.entry_points().select(group="oarepo.models"):
        ret[ep.name] = load_model_from_entrypoint(ep)
    return ret


def load_model(
    model_filename,
    package=None,
    configs=(),
    black=True,
    isort=True,
    sets=(),
    model_content=None,
    extra_included=None,
):
    loaders = load_entry_points_dict("oarepo_model_builder.loaders")
    included_models = load_included_models_from_entry_points()
    if extra_included:
        included_models.update(extra_included)
    schema = ModelSchema(
        model_filename,
        content=model_content,
        loaders=loaders,
        included_models=included_models,
    )
    for config in configs:
        load_config(schema, config, loaders)
    for s in sets:
        k, v = s.split("=", 1)
        schema.schema[k] = v
    check_plugin_packages(schema)
    if package:
        schema.settings["package"] = package
    if "python" not in schema.settings:
        schema.settings.python = HyphenMunch()
    schema.settings.python.use_isort = isort
    schema.settings.python.use_black = black
    return schema


def load_config(schema, config, loaders):
    old_loaders = schema.loaders
    schema.loaders = loaders
    try:
        loaded_file = schema._load(config)
        schema.merge(loaded_file)
    finally:
        schema.loaders = old_loaders


def check_plugin_packages(schema):
    try:
        required_packages = schema.schema.plugins.packages
    except AttributeError:
        return
    import subprocess

    import pkg_resources

    known_packages = set(d.project_name for d in pkg_resources.working_set)
    unknown_packages = [rp for rp in required_packages if rp not in known_packages]
    if unknown_packages:
        if (
            input(
                f'Required packages {", ".join(unknown_packages)} are missing. '
                f"Should I install them for you via pip install? (y/n) "
            )
            == "y"
        ):
            if subprocess.call(["pip", "install", *unknown_packages]):
                sys.exit(1)
            print("Installed required packages, please run this command again")
        sys.exit(1)
