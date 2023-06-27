import dataclasses
from typing import Dict, List, Optional


@dataclasses.dataclass
class FacetDefinition:
    path: str
    dot_path: str
    searchable: bool
    imports: List[Dict[str, str]]
    field: Optional[str] = None

    def update(self, facet_section):
        self.imports.extend(facet_section.get("imports", []))
        if self.searchable is None:
            # searchable not set up, so take it from argument
            self.searchable = facet_section.get("searchable", None)

    def set_field(self, facet_section, arguments, field_class=None):
        field = facet_section.get("field")
        if field:
            self.field = field
        else:
            if not field_class:
                field_class = facet_section.get("facet-class")
            if field_class:
                self.field = f"{field_class}({', '.join(arguments)})"
