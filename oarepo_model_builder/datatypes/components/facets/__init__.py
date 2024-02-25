import dataclasses
from typing import Dict, List, Optional

from oarepo_model_builder.utils.jinja import (
    extract_extra_code_imports,
    generate_extra_code,
)
from oarepo_model_builder.utils.python_name import PythonQualifiedName


@dataclasses.dataclass
class FacetDefinition:
    path: str
    dot_path: str
    searchable: bool
    imports: List[Dict[str, str]]
    facet_groups: Dict[str, int]
    facet: Optional[bool]
    field: Optional[str] = None

    def update(self, facet_section):
        self.imports.extend(facet_section.get("imports", []))
        if self.searchable is None:
            # searchable not set up, so take it from argument
            self.searchable = facet_section.get("searchable", None)

    def set_field(self, facet_section, arguments, field_class=None):
        field = facet_section.get("field")
        extra_imports = None
        if field:
            extra_imports = extract_extra_code_imports(field)
            self.field = generate_extra_code(field)
        else:
            if not field_class:
                field_class = facet_section.get("facet-class")
            if field_class:
                field_class = PythonQualifiedName(field_class)
                self.field = f"{field_class.local_name}({', '.join(arguments)})"
                extra_imports = field_class.imports

        if extra_imports:
            self.imports = [*self.imports, *extra_imports]
