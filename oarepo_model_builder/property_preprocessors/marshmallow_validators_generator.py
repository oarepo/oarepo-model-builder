from oarepo_model_builder.invenio.invenio_record_schema import InvenioRecordSchemaBuilder
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack
from oarepo_model_builder.utils.deepmerge import deepmerge


class ValidatorsPreprocessor(PropertyPreprocessor):
    @process(
        model_builder=InvenioRecordSchemaBuilder,
        path="**/properties/*",
    )
    def validators_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):
        try:
            definition = data['oarepo:marshmallow']
            validators = definition['validators']
        except:
            validators = []
        try:
            minimum = data.get("minimum", None)
            maximum = data.get("maximum", None)
            exclusive_minimum = data.get("exclusiveMinimum", None)
            exclusive_maximum = data.get("exclusiveMaximum", None)

            if minimum is not None or maximum is not None or exclusive_minimum is not None or exclusive_maximum is not None:
                validators.append(
                    f"ma_valid.Range("
                    f'min={minimum or exclusive_minimum or "None"}, max={maximum or exclusive_maximum or "None"}, '
                    f"min_inclusive={exclusive_minimum is None}, max_inclusive={exclusive_maximum is None})"
                )
            min_length = data.get("minLength", None)
            max_length = data.get("maxLength", None)
            required = data.get("required", False)
            if required:
                deepmerge(
                    data.setdefault("oarepo:marshmallow", {}),
                    {'required': True},
                )
                print(type(data))
            if min_length is not None or max_length is not None:
                validators.append(f"ma_valid.Length(min={min_length}, max={max_length})")

            if len(validators) > 0:

                deepmerge(
                    data["oarepo:marshmallow"].setdefault("validators", []),
                    validators,
                )
        except:
            pass

        return data


