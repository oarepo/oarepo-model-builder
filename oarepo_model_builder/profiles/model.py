from pathlib import Path
from typing import Union

import json5

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.entrypoints import (create_builder_from_entrypoints,
                                              load_model)
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.profiles import Profile
from oarepo_model_builder.profiles.extend import ExtendProfile
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.utils.deepmerge import deepmerge


class ModelProfile(Profile):
    def build(
        self,
        model: ModelSchema,
        output_directory: Union[str, Path],
        builder: ModelBuilder,
    ):
        # at first handle "extend"
        if "extend" in model.current_model:
            self.handle_extend(model.current_model.extend, model, builder)
        return super().build(model, output_directory, builder)

    def handle_extend(
        self, extended_schema: str, model: ModelSchema, builder: ModelBuilder
    ):
        """
        extending the model means:
            1. extended schema is read as a schema. If there is a json path behind it,
               it is used to select the model. by default /model is taken
            2. The model will be processed through "extend" profile with
               the output file "model.json5" stored in memory:
                  * properties ending with "-class" on model will be turned to array and suffix changed to -base-classes
                  * jsonschema and mapping will not be touched
                  * marshmallow will have all the properties marked as {read: false, write: false} so that they are not generated
            3. the resulting model will be merged as if use: was used
        """

        extended_schema = extended_schema.split("#", maxsplit=1)
        schema_location = extended_schema[0]
        if len(extended_schema) == 1:
            model_field = "model"
        else:
            model_field = extended_schema[1]
            if model_field.startswith("/"):
                model_field = model_field[1:]
            if "/" in model_field:
                raise ValueError("Can not currently process nested models")

        extended_model = load_model(
            schema_location,
            package=None,
            configs=[],
            black=False,
            isort=False,
            sets=[],
            extra_included=model.included_schemas,
        )
        extended_model.model_field = model_field

        fs = InMemoryFileSystem()
        builder = create_builder_from_entrypoints(
            profile="extend",
            conflict_resolver=builder.conflict_resolver,
            overwrite=builder.overwrite,
            filesystem=fs,
        )

        ExtendProfile().build(extended_model, "", builder)

        loaded_model = json5.loads(fs.read("model.json5"))
        deepmerge(model.current_model, loaded_model)
