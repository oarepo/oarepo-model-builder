from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
import marshmallow as ma


class SavedModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        saved_model_file = ma.fields.String(
            attribute="saved-model-file",
            data_key="saved-model-file",
            required=False,
        )
