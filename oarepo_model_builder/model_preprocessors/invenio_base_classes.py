from oarepo_model_builder.model_preprocessors import ModelPreprocessor
from oarepo_model_builder.utils.camelcase import camel_case, snake_case
from oarepo_model_builder.utils.deepmerge import deepmerge

class InvenioBaseClassesModelPreprocessor(ModelPreprocessor):
    TYPE = "invenio_base_classes"

    def transform(self, schema, settings):
        settings.python.setdefault("record-resource-class-bases", []).append(
            "invenio_records_resources.resources.RecordResource")
        settings.python.setdefault("record-resource-config-class-bases", []).append(
            "invenio_records_resources.resources.RecordResourceConfig")
        settings.python.setdefault("record-service-bases", []).append(
            "invenio_records_resources.services.RecordService")
        settings.python.setdefault("record-bases", []).append(
            "invenio_records_resources.records.api.Record")
        settings.python.setdefault("record-service-config-bases", []).append(
            "invenio_records_resources.services.RecordServiceConfig")