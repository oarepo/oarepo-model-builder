from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
import marshmallow as ma


class ResourceModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        collection_url = ma.fields.String(
            data_key="collection-url",
            required=False,
            attribute="collection-url",
        )
