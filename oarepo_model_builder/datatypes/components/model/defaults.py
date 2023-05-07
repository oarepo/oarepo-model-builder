import os
from pathlib import Path

import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.utils.camelcase import camel_case, snake_case
from oarepo_model_builder.utils.python_name import split_base_name

from .utils import set_default


class ModuleSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

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

        kebap_module = ma.fields.String(
            attribute="kebap-module",
            data_key="kebap-module",
            metadata={"doc": "Kebap case of the module"},
        )

        prefix = ma.fields.String(
            metadata={"doc": "Prefix that will be applied to class names"}
        )
        prefix_upper = ma.fields.String(
            metadata={"doc": "Uppercase variant of the prefix"}
        )
        prefix_snake = ma.fields.String(metadata={"doc": "Snake variant of the prefix"})

        suffix = ma.fields.String(
            metadata={"doc": "Suffix that will be applied to various names"}
        )
        suffix_upper = ma.fields.String(
            metadata={"doc": "Uppercase variant of the suffix"}
        )
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
        profile = ma.fields.String(
            attribute="profile-name",
            data_key="profile-name",
            metadata={"doc": "Actual profile"},
        )

    def before_model_prepare(self, datatype, **kwargs):
        model_name = set_default(
            datatype,
            "model-name",
            lambda model: os.path.basename(
                schema.schema.get("output-directory", os.getcwd())
            ),
        )
        module_container = set_default(datatype, "module", {})
        module = module_container.setdefault("module", model_name.replace("-", "_"))

        module_path = module.split(".")
        module_container.setdefault(
            "path", str(Path(module_path[0]).joinpath(*module_path[1:]))
        )

        base = module_container.setdefault(
            "base",
            split_base_name(module),
        )
        base_upper = module_container.setdefault(
            "base-upper",
            module_base.upper(),
        )
        module_container.setdefault(
            "kebap-module",
            module.replace("_", "-"),
        )

        prefix = module_container.setdefault(
            "prefix",
            camel_case(module_base),
        )
        prefix_upper = module_container.setdefault(
            "prefix-upper",
            prefix.upper(),
        )
        prefix_snake = module_container.setdefault(
            "prefix",
            snake_case(prefix),
        )

        suffix = module_container.setdefault(
            "suffix",
            snake_case(prefix),
        )
        suffix_upper = module_container.setdefault(
            "suffix-upper",
            suffix.upper(),
        )
        suffix_snake = module_container.setdefault(
            "suffix",
            snake_case(suffix),
        )

        set_default(datatype, "profile-name", "records")
