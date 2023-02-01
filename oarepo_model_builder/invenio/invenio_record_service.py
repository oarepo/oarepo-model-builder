from .invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.utils.hyphen_munch import HyphenMunch


class InvenioRecordServiceBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_service"
    class_config = "record-service-class"
    template = "record-service"
