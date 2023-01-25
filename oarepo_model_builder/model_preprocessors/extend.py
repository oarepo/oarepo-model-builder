import os
from pathlib import Path
from typing import Dict

from oarepo_model_builder.utils.jinja import split_base_name

from ..schema import ModelSchema
from . import ModelPreprocessor


class BaseClassesModelPreprocessor(ModelPreprocessor):
    TYPE = "extend-base-classes"

    def transform(self, schema: ModelSchema, settings: Dict):
        model = schema.model
        marshmallow = model.pop("marshmallow")
        for k in list(model.keys()):
            if k.endswith("-class"):
                prefix = k[:-6]
                model[f"{prefix}-bases"] = [model.pop(k)]
            elif k not in ("type", "properties"):
                model.pop(k)  # pop all other stuff
        model["marshmallow"] = {"base-classes": [marshmallow["schema-class"]]}
