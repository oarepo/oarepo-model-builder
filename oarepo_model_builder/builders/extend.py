from .json_base import JSONBaseBuilder


class ExtendBuilder(JSONBaseBuilder):
    TYPE = "extend"
    output_file_type = "json"

    def build_node(self, node):
        generated = self.generate(node)
        # on model, move the marshmallow class into base_classes
        self._process_top_level_marshmallow(generated)
        generated["type"] = "object"
        self.output.merge(generated)

    def generate(self, node):
        ret = {**node.definition}
        ret.pop("properties", None)
        ret.pop("items", None)

        self._process_marshmallow_def(ret.setdefault("marshmallow", {}))
        self._process_marshmallow_def(
            ret.setdefault("ui", {}).setdefault("marshmallow", {})
        )

        if getattr(node, "children", None):
            properties = ret.setdefault("properties", {})
            for k, v in node.children.items():
                v = self.generate(v)
                properties[k] = v
        if getattr(node, "item", None):
            ret["items"] = self.generate(node.item)
        return ret

    def _process_marshmallow_def(self, marshmallow):
        marshmallow.update({"read": False, "write": False})
        if "class" in marshmallow:
            # already generated - if user wants to override this, he has to set schema-class and generate
            marshmallow["generate"] = False

    def _process_top_level_marshmallow(self, model):
        marshmallow = model.pop("marshmallow")
        ui = model.pop("ui")

        for k in list(model.keys()):
            if k.endswith("-class"):
                prefix = k[:-6]
                model[f"{prefix}-bases"] = [model.pop(k)]
            elif k not in ("type", "properties"):
                model.pop(k)  # pop all other stuff

        model["marshmallow"] = {"base-classes": [marshmallow["class"]]}
        model["ui"] = {"marshmallow": {"base-classes": [ui["marshmallow"]["class"]]}}

    def begin(self, current_model, schema):
        super(JSONBaseBuilder, self).begin(current_model, schema)
        self.output = self.builder.get_output(self.output_file_type, "model.json5")

    def finish(self):
        # force clean output
        super().finish()
        self.output.force_clean_output()
