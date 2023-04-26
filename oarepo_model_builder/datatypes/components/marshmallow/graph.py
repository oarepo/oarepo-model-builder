import dataclasses
from typing import List, Dict, Optional
from ...datatypes import Import
from ....utils.jinja import base_name


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
    owner: "MarshmallowClass"
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
    order: int = None

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
            raise Exception("Cycle found, code missing")
        else:
            for c in for_another_round:
                c.remove_references(processed_class_names)
        to_process = for_another_round
    classes_list.sort(key=lambda x: [-x.order, x.class_name])


def collect_imports(current_package_name, classes_list: List[MarshmallowClass]):
    for cls in classes_list:
        for fld in cls.fields:
            if not fld.reference:
                continue
            if fld.reference.accessor:
                # local accessor handles its own imports inside the accessor
                continue
            # if from different package, 
            if package_name(fld.reference) != current_package_name:
                cls.imports.append(Import(import_path=fld.reference))
    