from jinja2 import Environment, FunctionLoader
from oarepo_model_builder.templates import templates
from oarepo_model_builder.builders import OutputBuilder
from ..outputs.json import JSONOutput
from ..utils.verbose import log


class CookiecutterBuilder(OutputBuilder):
    TYPE = "cookiecutter"

    def finish(self):
        super().finish()
        context = {"settings": self.schema.settings}

        output = self.builder.get_output(
            "diff", "cookiecutter.yaml")

        env = Environment(
            loader=FunctionLoader(
                lambda tn: templates.get_template(tn, context["settings"])),
            autoescape=False,
        )

        output.write(env.get_template("cookiecutter-config").render(context))
