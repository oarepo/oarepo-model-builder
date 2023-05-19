import dataclasses
from typing import List

import marshmallow as ma

from ..datatypes import Import, Section, datatypes
from .containers import ObjectDataType


@dataclasses.dataclass
class Link:
    name: str
    link_class: str = "RecordLink"
    link_args: List[str] = dataclasses.field(default_factory=list)
    imports: List[Import] = dataclasses.field(default_factory=list)

    @property
    def link_args_str(self):
        return ", ".join(x for x in self.link_args)


class ModelDataType(ObjectDataType):
    model_type = "model"
    json_schema = {"type": "object"}

    mapping = {}

    class ModelSchema(ObjectDataType.ModelSchema):
        type = ma.fields.Str(
            load_default="model",
            required=False,
            validate=ma.validate.Equal("model"),
        )

    def _process_mapping(self, section: Section, **kwargs):
        section.config = (
            {}
        )  # remove default stuff as mapping on model means not "properties"-level mapping, but root-level mapping
        if self.definition.get("searchable") is False:
            section.config["enabled"] = False
        else:
            section.config.setdefault("enabled", True)

    @property
    def section_global_mapping(self):
        return self.default_section_mapping

    @property
    def links(self):
        return {
            "links_item": [
                Link(
                    name="self",
                    link_class="RecordLink",
                    link_args=['"{self.url_prefix}{id}"'],
                    imports=[Import("invenio_records_resources.services.RecordLink")],
                ),
            ],
            "links_search": [
                Link(
                    name=None,
                    link_class="pagination_links",
                    link_args=['"{self.url_prefix}{?args*}"'],
                    imports=[
                        Import("invenio_records_resources.services.pagination_links")
                    ],
                ),
            ],
        }

    def prepare(self, context):
        datatypes.call_components(
            datatype=self, method="before_model_prepare", context=context
        )
        super().prepare(context)
        datatypes.call_components(
            datatype=self, method="after_model_prepare", context=context
        )
