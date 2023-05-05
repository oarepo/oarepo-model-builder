from oarepo_model_builder.outputs.python import PythonOutput

from ..datatypes import Section
from ..datatypes.model import Link
from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordServiceConfigBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_service_config"
    class_config = "record-service-config-class"
    template = "record-service-config"

    def process_template(self, python_path, template, **extra_kwargs):
        if self.parent_modules:
            self.create_parent_modules(python_path)
        output: PythonOutput = self.builder.get_output("python", python_path)

        record_schema_class = self.current_model.definition.get("marshmallow", {}).get(
            "schema-class", self.current_model.definition["record-schema-class"]
        )

        links_section: Section = self.current_model.section_links
        imports = set()
        link: Link
        for s in links_section.config.values():
            for link in s:
                imports.update(link.imports)
        imports = list(imports)
        imports.sort(key=lambda x: (x.import_path, x.alias or ""))

        for ll in links_section.config.values():
            ll.sort(key=lambda x: x.name or "")

        context = dict(
            settings=self.settings,
            current_model=self.current_model,
            record_schema_class=record_schema_class,
            links=links_section.config,
            link_imports=imports,
            **extra_kwargs,
        )
        output.merge(template, context)
