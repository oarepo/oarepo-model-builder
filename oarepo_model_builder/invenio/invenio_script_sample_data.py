import json
from typing import Callable, List

import faker
import faker.providers
from faker import Faker
from jinja2 import Environment, FunctionLoader

from oarepo_model_builder.builders import OutputBuilder
from oarepo_model_builder.builders.utils import ensure_directory
from oarepo_model_builder.templates import templates

from ..builder import ModelBuilder
from ..builders import process
from ..builders.json_base import JSONBaseBuilder
from ..entrypoints import load_entry_points_list
from ..property_preprocessors import PropertyPreprocessor


class SampleDataGenerator(faker.Generator):
    def __init__(self, **config):
        super().__init__(**config)
        self.formatters = set()

    def set_formatter(self, name: str, method: Callable) -> None:
        self.formatters.add(name)
        return super().set_formatter(name, method)


# provider for Faker
class Provider:
    def __init__(self, generator) -> None:
        self.generator = generator

    def random_float(self):
        rnd = self.generator.random.randrange(-100, 100 + 1, 1)
        return rnd / 10

    def sample_object(self):
        return {
            self.generator.word(): self.generator.word()
            for _ in range(self.generator.random.randrange(1, 5, 1))
        }

    def constant(self, value=None):
        return value

    def language_dict(self):
        return {lang: Faker(locale=lang).sentence() for lang in ("cs", "en")}


SKIP = "skip"


class InvenioScriptSampleDataBuilder(JSONBaseBuilder):
    TYPE = "script_sample_data"
    output_file_type = "yaml"
    output_file_name = "script-import-sample-data"
    parent_module_root_name = "jsonschemas"

    def __init__(
        self, builder: ModelBuilder, property_preprocessors: List[PropertyPreprocessor]
    ):
        super().__init__(builder, property_preprocessors)
        self.generator = SampleDataGenerator()
        from faker.config import PROVIDERS

        self.faker = faker.Faker(
            generator=self.generator,
            providers=[
                "oarepo_model_builder.invenio.invenio_script_sample_data",
                *PROVIDERS,
            ],
        )

        self.sample_data_providers = load_entry_points_list(
            "oarepo_model_builder.sample_data_providers"
        ) + [faker_provider]

    @process("/model/**", condition=lambda current, stack: stack.schema_valid)
    def model_element(self):
        schema_element_type = self.stack.top.schema_element_type

        if schema_element_type == "property":
            self.generate_property(self.stack.top.key)
        elif schema_element_type == "items":
            # the count is in the oarepo:sample section above the "items" element, so need to look at [-2], not the top
            count = self.get_count(self.stack[-2].data, None)
            if count is None:
                count = self.faker.random_int(1, 5)
            for key in range(count):
                self.generate_property(key)
        else:
            self.build_children()

    def generate_property(self, key):
        if not self.skip(self.stack):
            if "properties" in self.stack.top.data:
                self.output.enter(key, {})
                self.build_children()
                self.output.leave()
            elif "items" in self.stack.top.data:
                self.output.enter(key, [])
                self.build_children()
                top = self.output.stack.real_top

                # make items unique, just for sure
                top_as_dict = {}
                for t in top:
                    top_as_dict[json.dumps(t, sort_keys=True)] = t
                top.clear()
                top.extend(top_as_dict.values())

                self.output.leave()
            else:
                self.output.primitive(key, self.generate_fake(self.stack))

    def build(self, schema):
        output_name = schema.settings[self.output_file_name]
        output = self.builder.get_output(self.output_file_type, output_name)
        if not output.created:
            return
        count = self.get_count(schema.schema)
        for _ in range(count):
            super().build(schema)

    def get_count(self, schema, default_count=50):
        return schema.get("oarepo:sample", {}).get("count", default_count)

    def skip(self, stack):
        return get_oarepo_sample(stack).get("skip", False)

    def on_enter_model(self, output_name):
        self.output.next_document()

    def generate_fake(self, stack):
        params = {}
        method = None
        config = get_oarepo_sample(stack)
        params = config.get("params", params)

        for provider in self.sample_data_providers:
            ret = provider(self.faker, self.settings, stack, params)
            if ret is not SKIP:
                return ret


def get_oarepo_sample(stack):
    if isinstance(stack.top.data, dict) and "oarepo:sample" in stack.top.data:
        sample = stack.top.data.get("oarepo:sample")
        if isinstance(sample, dict):
            return sample
        if isinstance(sample, str):
            return {"faker": "constant", "params": {"value": sample}}
        if isinstance(sample, (list, dict)):
            if (
                stack.top.schema_element_type == "property"
                and "items" in stack.top.data
            ):
                return {
                    "faker": "random_elements",
                    "params": {"elements": sample, "unique": True},
                }
            else:
                return {"faker": "random_element", "params": {"elements": sample}}

    return {}


def faker_provider(faker, settings, stack, params):
    config = get_oarepo_sample(stack)
    method = config.get("faker")
    if not method:
        if stack.top.key in faker.formatters:
            method = stack.top.key
        else:
            data_type = stack.top.data.get("type")
            if data_type == "integer":
                method = "random_int"
            elif data_type == "number":
                method = "random_float"
            elif data_type == "date":
                method = "date"
            elif data_type == "object":
                # it is an object with unknown properties, return a sample object
                method = "sample_object"
            elif data_type in ("string", "keyword", "fulltext", "fulltext+keyword"):
                method = "sentence"
            else:
                print(
                    f"Warning: do not know how to generate sample data for {data_type} at path {stack.path}, using plain string rule"
                )
                method = "sentence"
    return getattr(faker, method)(**params)


class InvenioScriptSampleDataShellBuilder(OutputBuilder):
    TYPE = "invenio_script_sample_data_loader"

    def finish(self):
        context = {"settings": self.schema.settings}

        env = Environment(
            loader=FunctionLoader(
                lambda tn: templates.get_template(tn, context["settings"])
            ),
            autoescape=False,
        )

        ensure_directory(self.builder, "scripts")
        output = self.builder.get_output("diff", "scripts/load_sample_data.sh")
        output.write(
            env.get_template("script-import-sample-data-shell").render(context)
        )
        output.make_executable()
