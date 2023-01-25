from oarepo_model_builder.model_preprocessors import ModelPreprocessor


class InvenioBaseClassesModelPreprocessor(ModelPreprocessor):
    TYPE = "invenio_base_classes"

    def transform(self, schema, settings):
        self.set_default_and_append_if_not_present(
            schema.current_model,
            "record-resource-bases",
            [],
            "invenio_records_resources.resources.RecordResource",
        )
        self.set_default_and_append_if_not_present(
            schema.current_model,
            "record-resource-config-bases",
            [],
            "invenio_records_resources.resources.RecordResourceConfig",
        )
        self.set_default_and_append_if_not_present(
            schema.current_model,
            "record-service-bases",
            [],
            "invenio_records_resources.services.RecordService",
        )
        self.set_default_and_append_if_not_present(
            schema.current_model,
            "record-bases",
            [],
            "invenio_records_resources.records.api.Record",
        )
        self.set_default_and_append_if_not_present(
            schema.current_model,
            "record-service-config-bases",
            [],
            "invenio_records_resources.services.RecordServiceConfig",
        )
