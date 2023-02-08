import os
from pathlib import Path
from typing import Dict

from oarepo_model_builder.utils.camelcase import camel_case, snake_case
from oarepo_model_builder.utils.deepmerge import deepmerge
from oarepo_model_builder.utils.jinja import split_base_name

from ..schema import ModelSchema
from . import ModelPreprocessor


class DefaultValuesModelPreprocessor(ModelPreprocessor):
    TYPE = "default"

    def transform(self, schema: ModelSchema, settings: Dict):
        model = schema.current_model

        deepmerge(
            model,
            {
                "record-prefix": camel_case(split_base_name(model.package)),
            },
        )

        self.set(
            model,
            "package",
            lambda: os.path.basename(
                schema.schema.get("output-directory", os.getcwd())
            ).replace("-", "_"),
        )

        self.set(
            model,
            "package-base",
            lambda: split_base_name(model.package),
        )

        self.set(model, "package-base-upper", lambda: model.package_base.upper())

        self.set(model, "kebap-package", lambda: model.package.replace("_", "-"))

        @self.set(model, "package-path")
        def c():
            package_path = model.package.split(".")
            return Path(package_path[0]).joinpath(*package_path[1:])

        self.set(model, "schema-version", lambda: schema.schema.get("version", "1.0.0"))

        self.set(
            model,
            "schema-name",
            lambda: f"{snake_case(model.record_prefix)}-{model.schema_version}.json",
        )

        self.set(
            model,
            "schema-file",
            lambda: os.path.join(
                model.package_path, "records", "jsonschemas", model.schema_name
            ),
        )

        self.set(model, "mapping-package", lambda: f"{model.package}.records.mappings")

        self.set(
            model,
            "jsonschemas-package",
            lambda: f"{model.package}.records.jsonschemas",
        )

        self.set(
            model,
            "mapping-file",
            lambda: os.path.join(
                model.package_path,
                "records",
                "mappings",
                "os-v2",
                snake_case(model.record_prefix),
                model.schema_name,
            ),
        )

        self.set(model, "schema-server", lambda: "http://localhost/schemas/")

        self.set(
            model,
            "index-name",
            lambda: snake_case(model.record_prefix)
            + "-"
            + os.path.basename(model.mapping_file).replace(".json", ""),
        )

        self.set(model, "collection-url", lambda: f"/{model.kebap_package}/")
        self.set(model, "model-name", lambda: model.package_base)

        # for outputting the model
        self.set(
            model,
            "saved-model-file",
            lambda: model.package_path / "models" / "model.json",
        )

        self.set(
            model,
            "oarepo-models-setup-cfg",
            lambda: snake_case(model.record_prefix),
        )
