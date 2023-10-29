import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent


class EnumComponent(DataTypeComponent):
    class ModelSchema(ma.Schema):
        enum = ma.fields.List(
            ma.fields.Raw, metadata={"doc": "A list of possible values"}
        )

    def process_marshmallow(self, datatype, section, **kwargs):
        enum = datatype.definition.get("enum")
        if enum:
            section.config.setdefault("validators", []).append(
                f"{{{{marshmallow.validate.OneOf}}}}({repr(enum)})"
            )

    def process_ui(self, datatype, section, **kwargs):
        enum = datatype.definition.get("enum")
        if enum:
            section.config.setdefault("marshmallow", {}).setdefault(
                "validators", []
            ).append(f"{{{{marshmallow.validate.OneOf}}}}({repr(enum)})")
