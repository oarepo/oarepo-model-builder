import os

import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType

from .defaults import DefaultsModelComponent
from .utils import set_default


class SavedModelSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    file_ = ma.fields.Str(
        attribute="file",
        data_key="file",
        metadata={"doc": "File where to save the model"},
    )
    alias = ma.fields.String(
        metadata={"doc": "Alias under which the model is registered in setup.cfg"}
    )
    module = ma.fields.String(metadata={"doc": "Module where the file is saved"})


class SavedModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        saved_model = ma.fields.Nested(
            SavedModelSchema, attribute="saved-model", data_key="saved-model"
        )

    def before_model_prepare(self, datatype, context=None, **kwargs):
        profile = context.get("profile_module")
        file = f"{profile}.json"

        module_path = datatype.definition["module"]["path"]
        module = datatype.definition["module"]["qualified"]

        saved_model = set_default(datatype, "saved-model", {})

        saved_model.setdefault(
            "file",
            os.path.join(module_path, "models", file),
        )
        saved_model.setdefault(
            "module",
            f"{module}.models",
        )
        saved_model.setdefault("alias", datatype.definition["module"]["alias"])
