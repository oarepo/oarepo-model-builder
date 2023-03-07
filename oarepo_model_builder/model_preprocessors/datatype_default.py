from oarepo_model_builder.datatypes import datatypes

from . import DeepTransformationModelPreprocessor


class DatatypeDefaultModelPreprocessor(DeepTransformationModelPreprocessor):
    def begin(self, schema, settings):
        super().begin(schema, settings)
        self.context = {}

    def transform_node(self, stack, data):
        if stack.top.schema_element_type in ("property", "items"):
            # stack top is property or items
            datatype = datatypes.get_datatype(
                data, stack.top.key, self.schema.current_model, self.schema, stack
            )
            if datatype:
                datatype.prepare(self.context)
