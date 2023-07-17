import dataclasses
from typing import List, Optional, Set

from oarepo_model_builder.validation import InvalidModelException

from ....utils.python_name import base_name, package_name
from ...datatypes import Import


@dataclasses.dataclass
class MarshmallowField:
    key: str
    definition: str
    imports: List[Import] = dataclasses.field(default_factory=list)
    owner: "MarshmallowClass" = None
    reference: "MarshmallowReference" = None

    @property
    def full_definition(self):
        if not self.reference:
            return self.definition
        return self.reference.apply(self.definition)


@dataclasses.dataclass
class MarshmallowReference:
    reference: str
    referenced_class: "MarshmallowClass" = None
    accessor: Optional[str] = None

    def set_class(self, classes):
        if self.reference in classes:
            self.referenced_class = classes[self.reference]

    def apply(self, definition):
        if self.accessor:
            ref = self.accessor
        else:
            ref = f"lambda: {base_name(self.reference)}()"

        return definition.replace("__reference__", ref)


@dataclasses.dataclass
class MarshmallowClass:
    class_name: str
    base_classes: List[str]
    imports: List[Import]
    fields: List[MarshmallowField]
    strict: bool
    order: Optional[int] = None

    references: List[MarshmallowReference] = dataclasses.field(default_factory=list)

    def collect_references(self, classes):
        references = []
        for fld in self.fields:
            if fld.reference and fld.reference.reference in classes:
                fld.reference.set_class(classes)
                references.append(fld.reference)
        self.references = references

    def remove_references(self, class_names):
        self.references = list(
            filter(lambda r: r.reference not in class_names, self.references)
        )


def sort_by_reference_count(classes_list: List[MarshmallowClass]):
    classes = {x.class_name: x for x in classes_list}
    to_process = list(classes_list)
    processed_class_names = set()

    for c in classes_list:
        c.collect_references(classes)

    order = 0
    while to_process:
        order += 1
        for_another_round = []
        for c in to_process:
            if c.references:
                for_another_round.append(c)
            else:
                processed_class_names.add(c.class_name)
                c.order = order
        if len(for_another_round) == len(to_process):
            raise InvalidModelException("Cycle found, code missing")
        else:
            for c in for_another_round:
                c.remove_references(processed_class_names)
        to_process = for_another_round
    classes_list.sort(key=lambda x: [-x.order, x.class_name])


def collect_imports(current_module, classes_list: List[MarshmallowClass]):
    for cls in classes_list:
        for fld in cls.fields:
            if not fld.reference or not fld.reference.reference:
                continue
            if fld.reference.accessor:
                # local accessor handles its own imports inside the accessor
                continue
            # if from different package,
            if package_name(fld.reference.reference) != current_module:
                fld.imports.append(Import(import_path=fld.reference.reference))


@dataclasses.dataclass
class PackageWithDependencies:
    package: str
    direct_dependencies: Set[str] = dataclasses.field(default_factory=set)
    accessor_dependencies: Set[str] = dataclasses.field(default_factory=set)
    dependencies: Set[str] = dataclasses.field(default_factory=set)

    def add_dependency(self, dependency: str):
        self.dependencies.add(dependency)

    def remove_dependencies(self, dependencies):
        for dep in dependencies:
            if dep in self.dependencies:
                self.direct_dependencies.add(dep)
                self.dependencies.remove(dep)

    def break_dependencies(self):
        self.accessor_dependencies.update(self.dependencies)
        self.dependencies.clear()


def set_package_dependencies(classes_by_package):
    package_dependencies: List[PackageWithDependencies] = []
    for p in classes_by_package:
        pd = PackageWithDependencies(p)
        package_dependencies.append(pd)
        for pc in classes_by_package[p]:
            for fld in pc.fields:
                if not fld.reference:
                    continue
                referenced_package = package_name(fld.reference.reference)
                if referenced_package != p and referenced_package in classes_by_package:
                    pd.add_dependency(referenced_package)
    to_process = list(package_dependencies)
    processed_dependencies = set()
    while to_process:
        for_another_round = []
        for c in to_process:
            if c.dependencies:
                for_another_round.append(c)
            else:
                processed_dependencies.add(c.package)
        if len(for_another_round) == len(to_process):
            raise InvalidModelException("Cycle found in packages, code missing")
        else:
            for c in for_another_round:
                c.remove_dependencies(processed_dependencies)
        to_process = for_another_round

    for p in package_dependencies:
        for cls in classes_by_package[p.package]:
            for fld in cls.fields:
                if not fld.reference:
                    continue
                reference_package_name = package_name(fld.reference.reference)
                if reference_package_name in p.direct_dependencies:
                    fld.imports.append(Import(fld.reference.reference))
                elif reference_package_name in p.accessor_dependencies:
                    fld.reference.accessor = f"get{base_name(fld.reference.reference)}"
