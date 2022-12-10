from pathlib import Path
from typing import Union

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.schema import ModelSchema


class Profile:
    def build(
        self,
        model: ModelSchema,
        output_directory: Union[str, Path],
        builder: ModelBuilder,
    ):
        builder.build(model, output_directory)
