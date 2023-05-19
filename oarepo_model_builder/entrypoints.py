import importlib.resources
import sys
from functools import reduce
from importlib import import_module
from pathlib import Path

import importlib_metadata

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.schema import ModelSchema, remove_star_keys


def create_builder_from_entrypoints(profile="record", **kwargs):
    # output classes do not depend on profile
    output_classes = load_entry_points_list("oarepo_model_builder.outputs", None)
    builder_classes = load_entry_points_list("oarepo_model_builder.builders", profile)

    return ModelBuilder(
        output_builders=builder_classes,
        outputs=output_classes,
        **kwargs,
    )


def load_entry_points_dict(name):
    return {
        ep.name: ep.load()
        for ep in importlib_metadata.entry_points().select(group=name)
    }


def load_entry_points_list(name, profile):
    ret = []
    loaded = {}
    group_name = f"{name}.{profile}" if profile else name
    load_from_entry_point_internal(name, group_name, loaded, ret)
    # inherit
    inherit_group = f"{name}.{profile}.inherit" if profile else f"{name}.inherit"
    for ep in importlib_metadata.entry_points().select(group=inherit_group):
        inherit_from = ep.value
        load_from_entry_point_internal(name, inherit_from, loaded, ret)
    ret.sort()
    return [x[1] for x in ret]


def load_from_entry_point_internal(name, group_name, loaded_keys, loaded_entries):
    for ep in importlib_metadata.entry_points().select(group=group_name):
        if ep.name in loaded_keys:
            print(
                f"WARNING: Entry point {ep.name} has already been registered to group {name}. "
                f"Previous value {loaded_keys[ep.name]}, new ignored value {ep.value}"
            )
            continue
        loaded_entry_point = ep.load()
        loaded_entries.append((ep.name, loaded_entry_point))
        loaded_keys[ep.name] = ep.value


def load_model_from_entrypoint(ep: importlib_metadata.EntryPoint):
    def load(schema):
        try:
            loaded_schema = ep.load()
        except:  # NOSONAR intentionally broad
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
    configs=(),
    black=True,
    isort=True,
    autoflake=True,
    sets=(),
    model_content=None,
    extra_included=None,
    merged_models=None,
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
        merged_models=merged_models,
    )
    for config in configs:
        load_config(schema, config, loaders)
    for s in sets:
        k, v = s.split("=", 1)
        schema.schema[k] = v
    check_plugin_packages(schema)
    if "python" not in schema.settings:
        schema.settings["python"] = {}
    schema.settings["python"]["use-isort"] = isort
    schema.settings["python"]["use-black"] = black
    schema.settings["python"]["use-autoflake"] = autoflake
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
