from typing import Iterator

from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class EDTFIntervalDumperBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "edtf_interval_dumper"
    section = "edtf-interval-dumper"
    template = "edtf-interval-record-dumper"

    def finish(self, **extra_kwargs):
        paths = list(self.get_paths(self.current_model.children))
        extra_kwargs["paths"] = sorted(set(paths))
        super().finish(**extra_kwargs)

    def get_paths(self, parent_node) -> Iterator[str]:
        children = parent_node
        for c in children:
            node = children[c]
            if (
                node.model_type == "edtf-interval"
                or node.model_type == "edtf-time-interval"
            ):
                yield self.to_path(node.path)
            elif node.children != {}:
                yield from self.get_paths(node.children)
            elif hasattr(node, "item"):
                yield from self.get_paths({"item": node.item})

    def to_path(self, path):
        components = path.split(".")
        return "/".join(components)
