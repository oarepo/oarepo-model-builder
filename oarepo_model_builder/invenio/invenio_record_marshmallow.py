from collections import defaultdict
from typing import List

from oarepo_model_builder.datatypes import DataType, datatypes
from oarepo_model_builder.datatypes.components.marshmallow.graph import (
    collect_imports,
    set_package_dependencies,
    sort_by_reference_count,
)
from oarepo_model_builder.datatypes.components.marshmallow.object import (
    MarshmallowClass,
)
from oarepo_model_builder.utils.jinja import package_name

from .invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordMarshmallowBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_schema"
    template = "marshmallow"
    extra_imports = []
    build_class_method = "marshmallow_build_class"
    skip_if_not_generating = False

    def build_node(self, node: DataType):
        # everything is done in finish
        pass

    def finish(self, **extra_kwargs):
        classes: List[MarshmallowClass] = self._generate_classes(self.current_model)
        classes.sort(
            key=lambda x: (
                "Metadata" in x.class_name,
                "Record" in x.class_name,
                x.class_name,
            )
        )
        classes_by_packages = defaultdict(list)
        for cls in classes:
            classes_by_packages[package_name(cls.class_name)].append(cls)
        for single_package_classes in classes_by_packages.values():
            sort_by_reference_count(single_package_classes)
        if len(classes_by_packages.keys()) > 1:
            set_package_dependencies(classes_by_packages)

        for pn, single_package_classes in classes_by_packages.items():
            collect_imports(pn, single_package_classes)
            # generate and merge python source
            self.generate_package(pn, single_package_classes)
        # files were generated, so we are not calling super().finish() here

    def _generate_classes(self, node: DataType):
        classes = []
        to_process = [node]
        while to_process:
            n = to_process.pop(0)

            marshmallow_section = n.section_marshmallow
            if marshmallow_section.config.get(
                "class"
            ) and marshmallow_section.config.get("generate", True):
                datatypes.call_components(
                    n,
                    self.build_class_method,
                    classes=classes,
                )
            if marshmallow_section.config.get("generate", True):
                to_process.extend(marshmallow_section.children.values())
                if marshmallow_section.item:
                    to_process.append(marshmallow_section.item)
        return classes

    def generate_package(self, package_name, package_classes: List[MarshmallowClass]):
        python_path = self.class_to_path(f"{package_name}.Dummy")

        imports = [*self.extra_imports]

        for cls in package_classes:
            imports.extend(cls.imports)
            for fld in cls.fields:
                imports.extend(fld.imports)

        imports = list(
            sorted(set(imports), key=lambda x: (x.import_path or "", x.alias or ""))
        )

        self.process_template(
            python_path,
            self.template,
            current_module=package_name,
            imports=imports,
            generated_classes=package_classes,
        )
