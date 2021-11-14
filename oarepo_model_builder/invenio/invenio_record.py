from oarepo_model_builder.builders import OutputBuilder, process
from oarepo_model_builder.builders.utils import ensure_parent_modules
from oarepo_model_builder.stack import ModelBuilderStack


class InvenioRecordBuilder(OutputBuilder):
    output_builder_type = 'invenio_record'

