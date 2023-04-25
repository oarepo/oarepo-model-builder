from oarepo_model_builder.datatypes import DataType

from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordMarshmallowBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_schema"
    class_config = "record-schema-class"
    template = "record-schema"

    def build_node(self, node: DataType):
        print(node.section_marshmallow.fingerprint)
