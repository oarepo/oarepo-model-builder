from pathlib import Path
from typing import List, Union

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.profiles import Profile
from oarepo_model_builder.schema import ModelSchema
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

        # record has type "model" if not explicitly stated otherwise
        if "type" not in current_model:
            current_model["type"] = "model"

        return super().build(
            model, profile, model_path, output_directory, builder, **kwargs
        )
