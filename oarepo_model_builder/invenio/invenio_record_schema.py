from collections import defaultdict, namedtuple
import copy
import dataclasses
from typing import Any, Dict, List, Tuple

from oarepo_model_builder.builders import process
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.stack.stack import ModelBuilderStack
from oarepo_model_builder.utils.camelcase import camel_case
from oarepo_model_builder.utils.jinja import (
    split_package_base_name,
    split_package_name,
    split_base_name,
)
from oarepo_model_builder.validation import InvalidModelException

from .invenio_base import InvenioBaseClassPythonBuilder

OAREPO_MARSHMALLOW_PROPERTY = "oarepo:marshmallow"

Import = namedtuple("Import", "import_path,alias")
GeneratedField = namedtuple(
    "GeneratedField",
    "field_class, field_arguments, field_imports"
    # field_imports are List[Import]
)


@dataclasses.dataclass
class MarshmallowNode:
    schema: ModelSchema
    parent: "MarshmallowNode"
    stack: ModelBuilderStack

    read: bool
    write: bool

    field_name: str
    exact_field: str
    field_class: str
    field_arguments: List[str]

    imports: Dict[str, str]

    @classmethod
    def from_stack(cls, schema: ModelSchema, stack: ModelBuilderStack):
        definition = stack.top.data.get(OAREPO_MARSHMALLOW_PROPERTY, {})
        field_arguments = copy.copy(definition.get("arguments", []))
        validators = definition.get("validators", [])
        if validators:
            field_arguments.append(f"validate=[{', '.join(validators)}]")

        return cls(
            schema=schema,
            parent=None,
            # semi-shallow clone
            stack=stack.clone(),
            field_arguments=field_arguments,
            **cls._kwargs(definition, schema, stack),
        )

    @classmethod
    def _kwargs(cls, definition: Any, schema: ModelSchema, stack: ModelBuilderStack):
        return {
            "read": definition.get("read", True),
            "write": definition.get("write", True),
            "field_name": definition.get("field_name", stack.top.key),
            "exact_field": definition.get("field", None),
            "field_class": definition.get("field-class", None),
            "imports": definition.get("imports", []),
        }

    def get_imports(self) -> List[Import]:
        if not self.exact_field:
            generated_field_imports: List[Import] = self._field_imports
        else:
            generated_field_imports = []
        return [
            Import(k["import"], k.get("alias")) for k in self.imports
        ] + generated_field_imports

    @property
    def _field_imports(self) -> List[Import]:
        return self._field_generator(self).field_imports

    def prepare(self, package_name: str, _context: Dict[str, Any]):
        if self.field_class:
            self.field_class = self._get_class_name(package_name, self.field_class)

    @property
    def _field_generator(self):
        data_type = self.stack.top.json_schema_type
        if not data_type:
            raise InvalidModelException(f"No datatype defined on {self.stack.path}")
        generator = self.schema.settings.python.marshmallow.mapping.get(
            data_type, None
        ) or default_marshmallow_generators.get(data_type, None)
        if not generator:
            raise RuntimeError(f"No generator defined for datatype {data_type}")
        return generator

    @property
    def field(self):
        return f"{self.field_name} = {self._field_rhs}"

    @property
    def _field_rhs(self):
        if self.exact_field:
            return self.exact_field
        else:
            generated_field: GeneratedField = self._field_generator(self)
            rw_arguments = []
            if self.read and not self.write:
                rw_arguments.append("dump_only=True")
            elif self.write and not self.read:
                rw_arguments.append("load_only=True")
            return (
                f"{generated_field.field_class}"
                + f"({', '.join(generated_field.field_arguments + self.field_arguments + rw_arguments)})"
            )

    def _get_class_name(self, package_name: str, class_name: str):
        if "." not in class_name:
            return f"{package_name}.{class_name}"
        if class_name.startswith("."):
            package_path = package_name.split(".")
            while class_name.startswith("."):
                if package_path:
                    package_path = package_path[:-1]
                class_name = class_name[1:]
            if package_path:
                class_name = f"{'.'.join(package_path)}.{class_name}"
        return class_name


@dataclasses.dataclass
class CompositeMarshmallowNode(MarshmallowNode):

    fields: List["MarshmallowNode"]

    @classmethod
    def _kwargs(cls, definition: Any, schema: ModelSchema, stack: ModelBuilderStack):
        return {"fields": [], **super()._kwargs(definition, schema, stack)}

    def add_field(self, field: "MarshmallowNode"):
        field.parent = self
        self.fields.append(field)

    def walk(self):
        for fld in self.fields:
            if isinstance(fld, CompositeMarshmallowNode):
                yield from fld.walk()
            else:
                yield fld
        yield self


@dataclasses.dataclass
class ObjectMarshmallowNode(CompositeMarshmallowNode):
    generate: bool
    schema_class: str
    base_classes: List[str]

    @classmethod
    def _kwargs(cls, definition: Any, schema: ModelSchema, stack: ModelBuilderStack):
        return {
            "generate": definition.get("generate", True),
            "schema_class": definition.get("schema-class", None),
            "base_classes": definition.get("base-classes", ["ma.Schema"]),
            **super()._kwargs(definition, schema, stack),
        }

    def prepare(self, package_name: str, context: Dict[str, Any]):
        super().prepare(package_name, context)

        known_classes: Dict[str, str] = context.setdefault("known_classes", {})

        if self.exact_field or self.field_class:
            return

        schema_class = self.schema_class
        if not schema_class:
            schema_class = camel_case(self.stack.top.key)
        schema_class = self._get_class_name(package_name, schema_class)
        fingerprint = self.stack.fingerprint
        schema_class = self._find_unique_schema_class(known_classes, schema_class)

        known_classes[schema_class] = fingerprint
        self.schema_class = schema_class

    def _find_unique_schema_class(self, known_classes, schema_class):
        if schema_class in known_classes:
            # reuse class with the same fingerprint
            if self.stack.fingerprint != known_classes[schema_class]:
                for i in range(100):
                    candidate = f"{schema_class}_{i}"
                    if candidate not in known_classes:
                        schema_class = candidate
                        break
                    if self.stack.fingerprint == known_classes[candidate]:
                        schema_class = candidate
                        break
                else:
                    raise InvalidModelException(
                        f"Too many marshmallow classes with name {schema_class}. Please specify your own class names"
                    )

        return schema_class

    def generate_schema_class(self):
        if not self.generate:
            return None, None, None
        if not self.schema_class:
            return None, None, None

        field_list = []
        for fld in self.fields:
            if fld.read or fld.write:
                # and generate the field
                field_list.append(fld.field)

        package_name, base_class_name = split_package_base_name(self.schema_class)

        field_list = "\n    ".join(field_list)

        return (
            package_name,
            base_class_name,
            f"""
class {base_class_name}({", ".join(self.base_classes)}):
    \"""{base_class_name} schema.\"""
    {field_list}
""",
        )


@dataclasses.dataclass
class ArrayMarshmallowNode(CompositeMarshmallowNode):
    @property
    def _field_rhs(self):
        # wrap the child's RHS with list
        ret = self._first_child._field_rhs
        return f"ma_fields.List({ret})"

    @property
    def _field_generator(self):
        # do not return generator for array but for the contained item
        return self._first_child._field_generator

    @property
    def _field_imports(self) -> List[Import]:
        return self._first_child._field_imports

    @property
    def _first_child(self):
        if len(self.fields) != 1:
            raise InvalidModelException(
                f"No array items or too many array items at {self.stack.path}"
            )
        return self.fields[0]


class InvenioRecordSchemaBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_schema"
    class_config = "record-schema-class"
    template = "record-schema"

    marshmallow_stack: List[MarshmallowNode]

    def begin(self, schema, settings):
        super().begin(schema, settings)
        stack = ModelBuilderStack()
        stack.push("model", schema.model)

        self.marshmallow_stack = [ObjectMarshmallowNode.from_stack(schema, stack)]

    def finish(self):
        model_node = self.marshmallow_stack[0]

        # generate schema classes wherever they are not filled
        package_name = split_package_name(
            self.schema.settings.python.record_schema_class
        )

        generated_classes = defaultdict(list)
        generated_imports = defaultdict(set)

        context = {}
        for fld in model_node.walk():
            fld.prepare(package_name, context)
            if hasattr(fld, "generate_schema_class"):
                package, class_name, generated_class = fld.generate_schema_class()
                if class_name:
                    imports = generated_imports[package]
                    for _f in fld.walk():
                        imports.update(_f.get_imports())
                    generated_classes[package].append(generated_class)

        # create python files ...
        for package_name in generated_classes:
            python_path = self.class_to_path(f"{package_name}.Dummy")
            x: Import
            imports = [
                x
                for x in generated_imports[package_name]
                if split_package_name(x.import_path) != package_name
            ]

            self.process_template(
                python_path,
                self.template,
                current_package_name=package_name,
                imports=imports,
                generated_classes=generated_classes[package_name],
            )
        # super.finish not called as it is handled in the for loop above

    @process("/model/**", condition=lambda current, stack: stack.schema_valid)
    def enter_model_element(self):
        schema_element_type = self.stack.top.schema_element_type

        if schema_element_type in ("property", "items"):
            json_schema_type = self.stack.top.json_schema_type
            if json_schema_type in ("object", "nested"):
                node_class = ObjectMarshmallowNode
            elif json_schema_type == "array":
                node_class = ArrayMarshmallowNode
            else:
                # primitive value
                node_class = MarshmallowNode
            fld = node_class.from_stack(self.schema, self.stack)
            self.marshmallow_stack[-1].add_field(fld)
            self.marshmallow_stack.append(fld)
            self.build_children()
            self.marshmallow_stack.pop()
        else:
            self.build_children()


def marshmallow_string_generator(node: MarshmallowNode) -> GeneratedField:
    """
    Takes information from the node and returns a tuple of (field_class, arguments)
    """
    return GeneratedField("ma_fields.String", [], [])


def marshmallow_integer_generator(node: MarshmallowNode) -> GeneratedField:
    return GeneratedField("ma_fields.Integer", [], [])


def marshmallow_number_generator(node: MarshmallowNode) -> GeneratedField:
    return GeneratedField("ma_fields.Float", [], [])


def marshmallow_boolean_generator(node: MarshmallowNode) -> GeneratedField:
    return GeneratedField("ma_fields.Boolean", [], [])


def marshmallow_raw_generator(node: MarshmallowNode) -> GeneratedField:
    return GeneratedField("ma_fields.Raw", [], [])


def marshmallow_datestring_generator(node: MarshmallowNode) -> GeneratedField:
    return GeneratedField("mu_fields.ISODateString", [], [])


def marshmallow_object_generator(node: MarshmallowNode) -> GeneratedField:
    if not hasattr(node, "schema_class"):
        raise RuntimeError("Should not happen")
    return GeneratedField(
        "ma_fields.Nested",
        [f"lambda: {split_base_name(node.schema_class)}()"],
        [Import(node.schema_class, None)],
    )


# TODO: rest of supported schema types

default_marshmallow_generators = {
    "string": marshmallow_string_generator,
    "integer": marshmallow_integer_generator,
    "number": marshmallow_number_generator,
    "boolean": marshmallow_boolean_generator,
    "raw": marshmallow_raw_generator,
    "object": marshmallow_object_generator,
    "nested": marshmallow_object_generator,
    "date": marshmallow_datestring_generator,
}
