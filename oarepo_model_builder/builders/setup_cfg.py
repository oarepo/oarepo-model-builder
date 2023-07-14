from pkg_resources import parse_version

from oarepo_model_builder.builders import OutputBuilder
from oarepo_model_builder.outputs.cfg import CFGOutput


class SetupCfgBuilder(OutputBuilder):
    TYPE = "setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")
        output.setdefault(
            "metadata",
            "name",
            self.current_model.definition["module"]["base"].replace("_", "-"),
        )
        version = self.schema.get("version", "1.0.0dev1")
        output.setdefault("metadata", "version", version)
        if parse_version(output.get("metadata", "version").value) < parse_version(
            version
        ):
            output.set("metadata", "version", version)
        output.setdefault(
            "metadata",
            "description",
            f"Repository model for {self.current_model.definition['model-name']}",
        )
        output.setdefault("metadata", "authors", "")

        output.setdefault("options", "python", ">=3.9")
        try:
            ov = int(self.settings["oarepo-version"])
            output.add_dependency("oarepo", f">={ov},<{ov+1}")
        except ValueError:
            output.add_dependency("oarepo", self.settings["oarepo-version"])
        output.add_dependency("oarepo-runtime", ">=1.0.0")

        output.setdefault("options", "packages", "find:")

        output.setdefault(
            "options.package_data", "*", "*.json, *.rst, *.md, *.json5, *.jinja2"
        )

        if "runtime-dependencies" in self.schema:
            for dep, value in self.schema["runtime-dependencies"].items():
                if value[0] not in (">", "<", "="):
                    value = ">=" + value
                output.add_dependency(dep, value)

        if "dev-dependencies" in self.schema:
            for dep, value in self.schema["dev-dependencies"].items():
                if value[0] not in (">", "<", "="):
                    value = ">=" + value
                output.add_dependency(
                    dep, value, group="options.extras_require", section="devs"
                )
