import json
import random
from typing import Callable

import faker
import faker.providers
from faker import Faker

from oarepo_model_builder.datatypes import (
    ArrayDataType,
    DataType,
    ObjectDataType,
    Section,
)

from ..builder import ModelBuilder
from ..builders.json_base import JSONBaseBuilder
from ..entrypoints import load_entry_points_list


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

    def random_boolean(self):
        rnd = self.generator.random.randrange(0, 2, 1)
        return rnd == 1

    def random_html(self):
        html = ""
        i = 0
        while i < 4:
            tag = random.choice(["<p>", "<div>", "<span>"])
            content = "".join(Faker().sentence())
            html += f"{tag}{content}{tag[0]}/{tag[1:]}"
            i = i + 1
        return html

    def datetime(self):
        return self.generator.date_time_this_decade(
            tzinfo=self.generator.pytimezone()
        ).isoformat()

    def edtf(self):
        rnd = self.generator.random.randrange(0, 3)
        if rnd == 0:
            return self.generator.date()
        if rnd == 1:
            return self.generator.date("%Y")
        if rnd == 2:
            return self.generator.date("%Y-%m")

    def edtf_interval(self):
        a = [self.edtf(), self.edtf()]
        a.sort()
        return "/".join(a)

    def edtf_time(self):
        rnd = self.generator.random.randrange(0, 3)
        if rnd == 0:
            return self.generator.date()
        if rnd == 1:
            return self.generator.date("%Y")
        if rnd == 2:
            return self.generator.date("%Y-%m")

    def edtf_time_interval(self):
        a = [self.edtf(), self.edtf()]
        a.sort()
        return "/".join(a)

    def time(self):
        return self.generator.time()

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


class SampleDataBuilder(JSONBaseBuilder):
    TYPE = "script_sample_data"
    output_file_type = "yaml"
    output_file_name = ["sample", "file"]
    parent_module_root_name = "jsonschemas"

    def __init__(self, builder: ModelBuilder):
        super().__init__(builder)
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
            "oarepo_model_builder.sample_data_providers", profile=None
        ) + [faker_provider]

    def build_node(self, node: DataType):
        if not self.output.created:
            return

        sample: Section = node.section_sample
        for __ in range(sample.config.get("count", 10)):
            self.output.next_document()
            generated = self.generate_sample_for_node_and_children(node)
            self.output.merge(generated)

    def generate_sample_for_node_and_children(self, node):
        sample_section, sample = get_oarepo_sample(node)
        if "sample" in sample:
            return sample["sample"]
        if sample.get("skip"):
            return SKIP

        if isinstance(node, ObjectDataType):
            ret = {}
            for k, v in sample_section.children.items():
                v = self.generate_sample_for_node_and_children(v)
                if v is not SKIP:
                    ret[k] = v
        elif isinstance(node, ArrayDataType):
            count = sample.get("count")
            if count is None:
                count = self.faker.random_int(1, 5)
            ret = {}
            for __ in range(count):
                v = self.generate_sample_for_node_and_children(sample_section.item)
                if v is not SKIP:
                    ret[json.dumps(v, sort_keys=True)] = v
            ret = list(ret.values())
        else:
            ret = self.generate_fake(node, sample)
        return ret

    def generate_fake(self, node: DataType, config):
        params = {}
        method = None
        params = config.get("params", params)

        for provider in self.sample_data_providers:
            ret = provider(self.faker, node.schema.schema["settings"], node, params)
            if ret is not SKIP:
                return ret
        return SKIP


def get_oarepo_sample(node):
    sample_section = node.section_sample
    sample = sample_section.config

    if isinstance(sample, dict):
        return sample_section, sample
    if isinstance(sample, str):
        return sample_section, {"faker": "constant", "params": {"value": sample}}
    if isinstance(sample, (list, dict)):
        if not node.key:
            # array
            return sample_section, {
                "faker": "random_elements",
                "params": {"elements": sample, "unique": True},
            }
        else:
            # element
            return sample_section, {
                "faker": "random_element",
                "params": {"elements": sample},
            }

    return sample_section, {}


def faker_provider(faker, settings, node, params):
    __, config = get_oarepo_sample(node)
    method = config.get("faker")
    if not method:
        if node.key in faker.formatters:
            method = node.key
        else:
            data_type = node.model_type
            if data_type == "integer":
                method = "random_int"
            elif data_type == "number":
                method = "random_float"
            elif data_type == "html":
                method = "random_html"
            elif data_type == "double":
                method = "random_float"
            elif data_type == "float":
                method = "random_float"
            elif data_type == "boolean":
                method = "random_boolean"
            elif data_type == "date":
                method = "date"
            elif data_type == "datetime":
                method = "datetime"
            elif data_type == "time":
                method = "time"
            elif data_type == "edtf":
                method = "edtf"
            elif data_type == "edtf-interval":
                method = "edtf_interval"
            elif data_type == "edtf-time-interval":
                method = "edtf_time_interval"
            elif data_type == "edtf-time":
                method = "edtf_time"
            elif data_type == "object":
                # it is an object with unknown properties, return a sample object
                method = "sample_object"
            elif data_type in ("string", "keyword", "fulltext", "fulltext+keyword"):
                method = "sentence"
            else:
                print(
                    f"Warning: do not know how to generate sample data for {data_type} at path {node.path}, using plain string rule"
                )
                method = "sentence"
    return getattr(faker, method)(**params)
