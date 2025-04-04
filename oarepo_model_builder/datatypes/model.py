import dataclasses
from typing import List

import marshmallow as ma

from ..datatypes import Section, datatypes
from ..utils.links import url_prefix2link
from ..utils.python_name import Import
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
        url_prefix = url_prefix2link(self.definition["resource-config"]["base-url"])
        html_url_prefix = url_prefix2link(
            self.definition["resource-config"]["base-html-url"]
        )
        return {
            "links_item": [
                Link(
                    name="self",
                    link_class="RecordLink",
                    link_args=[
                        f'"{{+api}}{url_prefix}{{id}}"',
                        'when=has_permission("read")',
                    ],
                    imports=[
                        Import("invenio_records_resources.services.RecordLink"),
                        Import("oarepo_runtime.services.config.has_permission"),
                    ],
                ),
                Link(
                    name="self_html",
                    link_class="RecordLink",
                    link_args=[
                        f'"{{+ui}}{html_url_prefix}{{id}}"',
                        'when=has_permission("read")',
                    ],
                    imports=[
                        Import("invenio_records_resources.services.RecordLink"),
                        Import("oarepo_runtime.services.config.has_permission"),
                    ],
                ),
            ],
            "links_search_item": [
                Link(
                    name="self",
                    link_class="RecordLink",
                    link_args=[
                        f'"{{+api}}{url_prefix}{{id}}"',
                        'when=has_permission("read")',
                    ],
                    imports=[
                        Import("invenio_records_resources.services.RecordLink"),
                        Import("oarepo_runtime.services.config.has_permission"),
                    ],
                ),
                Link(
                    name="self_html",
                    link_class="RecordLink",
                    link_args=[
                        f'"{{+ui}}{html_url_prefix}{{id}}"',
                        'when=has_permission("read")',
                    ],
                    imports=[
                        Import("invenio_records_resources.services.RecordLink"),
                        Import("oarepo_runtime.services.config.has_permission"),
                    ],
                ),
            ],
            "links_search": [
                Link(
                    name=None,
                    link_class="pagination_links",
                    link_args=[f'"{{+api}}{url_prefix}{{?args*}}"'],
                    imports=[
                        Import("invenio_records_resources.services.pagination_links")
                    ],
                ),
                Link(
                    name=None,
                    link_class="pagination_links_html",
                    link_args=[f'"{{+ui}}{url_prefix}{{?args*}}"'],
                    imports=[
                        Import("oarepo_runtime.services.records.pagination_links_html")
                    ],
                ),
            ],
        }

    def prepare(self, context):
        if "profile" in context:
            self.profile = context["profile"]
        datatypes.call_components(
            datatype=self, method="before_model_prepare", context=context
        )
        super().prepare(context)
        datatypes.call_components(
            datatype=self, method="after_model_prepare", context=context
        )
