import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType

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


class SavedModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        saved_model = ma.fields.Nested(
            SavedModelSchema, attribute="saved-model", data_key="saved-model"
        )

    def before_model_prepare(self, datatype, **kwargs):
        module_path = datatype.definition["module-path"]
        saved_model = set_default(datatype, "saved-model", {})
        saved_model.setdefault(
            "file",
            os.path.join(model["module-path"], "models", "model.json"),
        )
        saved_model.setdefault("alias", snake_case(model["record-prefix"]))
