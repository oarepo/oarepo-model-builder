from pathlib import Path
from typing import Any, Dict, List, Union

import json5

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.profiles import Profile
from oarepo_model_builder.profiles.extend import ExtendProfile
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.utils.deepmerge import deepmerge
from oarepo_model_builder.utils.dict import dict_get


class RecordProfile(Profile):
    default_model_path = ("record",)

    def build(
        self,
        model: ModelSchema,
        profile: str,
        model_path: List[str],
        output_directory: Union[str, Path],
        builder: ModelBuilder,
        **kwargs,
    ):
        current_model = dict_get(model.schema, model_path)
        if "extend" in current_model:
            self.handle_extend(
                current_model["extend"],
                model,
                profile,
                model_path,
                current_model,
                builder,
            )
        return super().build(
            model, profile, model_path, output_directory, builder, **kwargs
        )

    def handle_extend(
        self,
        extended_schema: str,
        model: ModelSchema,
        profile: str,
        model_path: List[str],
        current_model: Dict[str, Any],
        builder: ModelBuilder,
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

        loaded_schema = {
            "record": {"use": [extended_schema]},
            "settings": model.settings,
        }

        extended_model = load_model(
            extended_schema.split("#", maxsplit=1)[0],
            configs=[],
            black=False,
            isort=False,
            autoflake=False,
            sets=[],
            extra_included=model.included_schemas,
            model_content=loaded_schema,
        )
        extended_model.model_field = "model"

        fs = InMemoryFileSystem()
        builder = create_builder_from_entrypoints(
            profile="extend",
            overwrite=builder.overwrite,
            filesystem=fs,
        )

        ExtendProfile().build(extended_model, profile, model_path, "", builder)

        loaded_model = json5.loads(fs.read("model.json5"))
        deepmerge(current_model, loaded_model)
