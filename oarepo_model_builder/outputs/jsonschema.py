from .json import JSONOutput


class JSONSchemaOutput(JSONOutput):
    TYPE = "jsonschema"

    def merge_jsonschema(self, jsonschema):
        self.stack.merge(jsonschema)

    def collect_required(self):
        top = self.stack.real_top
        # just a sanity check
        if not isinstance(top, dict):
            return
        if "properties" not in top:
            return
        required = []
        for prop_key, prop in top["properties"].items():
            if not isinstance(prop, dict):
                continue
            if not isinstance(prop.get("required"), list):
                if prop.pop("required", None):
                    required.append(prop_key)
        if required:
            required.sort()
            top["required"] = required
