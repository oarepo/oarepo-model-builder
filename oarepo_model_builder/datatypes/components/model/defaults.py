import os
from pathlib import Path

import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.utils.camelcase import camel_case, snake_case
from oarepo_model_builder.utils.python_name import (
    convert_name_to_python,
    split_base_name,
)

from .utils import set_default


class ModuleSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    alias = ma.fields.String(metadata={"doc": "Alias to use for setup.cfg etc."})
    qualified = ma.fields.String(
        metadata={"doc": "Module (fully qualified) where the model is generated"}
    )
    path = ma.fields.String(
        metadata={"doc": "Path on the filesystem with the top-level module"}
    )

    base = ma.fields.String(
        metadata={"doc": "Base name of the module (if the module has dot)"}
    )
    base_upper = ma.fields.String(
        attribute="base-upper",
        data_key="base-upper",
        metadata={"doc": "Uppercase of the base name"},
    )
    base_title = ma.fields.String(
        attribute="base-title",
        data_key="base-title",
        metadata={"doc": "Capitalized base name"},
    )
    kebab_module = ma.fields.String(
        attribute="kebab-module",
        data_key="kebab-module",
        metadata={"doc": "Kebab case of the module"},
    )

    prefix = ma.fields.String(
        metadata={"doc": "Prefix that will be applied to class names"}
    )
    prefix_upper = ma.fields.String(metadata={"doc": "Uppercase variant of the prefix"})
    prefix_snake = ma.fields.String(metadata={"doc": "Snake variant of the prefix"})

    suffix = ma.fields.String(
        metadata={"doc": "Suffix that will be applied to various names"}
    )
    suffix_upper = ma.fields.String(metadata={"doc": "Uppercase variant of the suffix"})
    suffix_snake = ma.fields.String(metadata={"doc": "Snake variant of the suffix"})


class DefaultsModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        model_name = ma.fields.String(
            attribute="model-name",
            data_key="model-name",
            metadata={
                "doc": "Name of the model, will be used as module name if no module is specified"
            },
        )
        module = ma.fields.Nested(
            ModuleSchema, metadata={"doc": "Model module details"}
        )

    def before_model_prepare(self, datatype, *, context, **kwargs):
        def get_model_name(_):
            model_name = datatype.definition.get("module", {}).get("qualified")
            if model_name:
                return model_name.rsplit(".", maxsplit=1)[-1].title()
            return os.path.basename(context.get("output-directory", os.getcwd()))

        model_name = set_default(datatype, "model-name", get_model_name)
        model_name = convert_name_to_python(model_name).lower()
        module_container = set_default(datatype, "module", {})

        module_container.setdefault("alias", model_name)
        module = module_container.setdefault("qualified", model_name)

        module_path = module.split(".")
        module_container.setdefault(
            "path", str(Path(module_path[0]).joinpath(*module_path[1:]))
        )

        module_base = module_container.setdefault(
            "base",
            split_base_name(module),
        )
        module_container.setdefault(
            "base-upper",
            module_base.upper(),
        )
        module_container.setdefault(
            "base-title",
            module_base.capitalize(),
        )
        module_container.setdefault(
            "kebab-module",
            module.replace(".", "-").replace("_", "-"),
        )

        prefix = module_container.setdefault(
            "prefix",
            camel_case(module_base),
        )
        module_container.setdefault(
            "prefix-upper",
            prefix.upper(),
        )
        module_container.setdefault(
            "prefix-snake",
            snake_case(prefix),
        )

        suffix = module_container.setdefault(
            "suffix",
            snake_case(prefix),
        )
        module_container.setdefault(
            "suffix-upper",
            suffix.upper(),
        )
        module_container.setdefault(
            "suffix-snake",
            snake_case(suffix),
        )
