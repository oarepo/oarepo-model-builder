import copy
import dataclasses
import logging
import re
from collections import defaultdict, namedtuple
from typing import Any, Dict, List, Tuple, Union

from oarepo_model_builder.builders import process
from oarepo_model_builder.builders.python import PythonBuilder
from oarepo_model_builder.datatypes import Import, datatypes
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.stack.stack import ModelBuilderStack
from oarepo_model_builder.utils.camelcase import camel_case
from oarepo_model_builder.utils.jinja import (
    split_base_name,
    split_package_base_name,
    split_package_name,
)
from oarepo_model_builder.validation import InvalidModelException

from .invenio_base import InvenioBaseClassPythonBuilder

log = logging.getLogger("invenio_record_schema")

BUILTIN_ALIASES = [
    "ma_validates",
    "ma",
    "ma_fields",
    "mu_fields",
    "mu_schemas",
]

OAREPO_MARSHMALLOW_PROPERTY = "marshmallow"


@dataclasses.dataclass
class MarshmallowNode:
    schema: Dict
    parent: "MarshmallowNode"
    stack: ModelBuilderStack

    read: bool
    write: bool

    field_name: str
    exact_field: str
    field_class: str
    field_arguments: List[str]
    field_imports: List[Import]
    imports: List[Dict[str, str]]
    used: bool = False

    @classmethod
    def from_stack(cls, schema: ModelSchema, stack: ModelBuilderStack):
        datatype = datatypes.get_datatype(
            stack.top.data, stack.top.key, schema.model, schema, stack
        )
        definition = datatype.marshmallow()
        imports = datatype.imports()
        field_arguments = copy.copy(definition.get("arguments", []))
        validators = definition.get("validators", [])
        if validators:
            field_arguments.append(f"validate=[{', '.join(validators)}]")

        constructor_arguments = dict(
            schema=schema,
            parent=None,
            # semi-shallow clone
            stack=stack.clone(),
            field_arguments=field_arguments,
            field_imports=imports,
            **cls._kwargs(definition, schema, stack),
        )
        return cls(**constructor_arguments)

    @classmethod
    def _kwargs(cls, definition: Any, schema: ModelSchema, stack: ModelBuilderStack):
        field_name = definition.get("field-name", stack.top.key)
        field_name = field_name.replace("-", "_")
        field_name = re.sub("\W", "", field_name)
        field_name = re.sub("^[^a-zA-Z_]+", "", field_name)
        return {
            "read": definition.get("read", True),
            "write": definition.get("write", True),
            "field_name": field_name,
            "exact_field": definition.get("field", None),
            "field_class": definition.get("field-class", None),
            "imports": definition.get("imports", []),
        }

    def get_imports(self) -> List[Import]:
        if not self.exact_field:
            generated_field_imports: List[Import] = list(self.field_imports)
        else:
            generated_field_imports = []
        return [
            Import(k["import"], k.get("alias")) for k in self.imports
        ] + generated_field_imports

    def prepare(self, package_name: str, _context: Dict[str, Any]):
        if self.field_class:
            self.field_class = self._get_class_name(package_name, self.field_class)

    @property
    def field(self):
        return f"{self.field_name} = {self._field_rhs}"

    @property
    def _field_rhs(self):
        if self.exact_field:
            return self.exact_field
        else:
            rw_arguments = []
            if self.read and not self.write:
                rw_arguments.append("dump_only=True")
            elif self.write and not self.read:
                rw_arguments.append("load_only=True")
            if self.stack.top.key != self.field_name:
                rw_arguments.append(f'data_key="{self.stack.top.key}"')
                rw_arguments.append(f'attribute="{self.stack.top.key}"')
            return (
                f"{self.field_class}"
                + f"({', '.join(self.field_arguments + rw_arguments)})"
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

    def mark_used(self):
        if self.read or self.write:
            self.used = True
        return self.used


@dataclasses.dataclass
class CompositeMarshmallowNode(MarshmallowNode):

    fields: List["MarshmallowNode"] = dataclasses.field(default_factory=list)

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

    def mark_used(self):
        if self.read or self.write:
            used = False
            for fld in self.fields:
                if fld.mark_used():
                    used = True
            self.used = used
        return self.used


@dataclasses.dataclass
class ObjectMarshmallowNode(CompositeMarshmallowNode):
    generate: bool = True
    schema_class: Union[str, None] = None
    base_classes: Union[List[str], None] = None

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

        if self.exact_field:
            return

        self.field_arguments = [
            f"lambda: {split_base_name(self.schema_class)}()"
        ] + self.field_arguments
        self.field_imports = [
            *self.field_imports,
            Import(import_path=self.schema_class, alias=None),
        ]

    def generate_schema_class(self):
        if not self.used:
            return None, None, None
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
        base_classes = []
        for x in self.base_classes:
            base_class_package_name, base_class_class_name = split_package_base_name(x)
            if base_class_package_name in BUILTIN_ALIASES:
                base_classes.append(x)
            else:
                base_classes.append(base_class_class_name)

        return (
            package_name,
            base_class_name,
            f"""
class {base_class_name}({", ".join(base_classes)}):
    \"""{base_class_name} schema.\"""
    {field_list}
""",
        )

    def get_imports(self) -> List[Import]:
        imports = super().get_imports()
        for base_class in self.base_classes:
            if "." in base_class:
                imports.append(Import(import_path=base_class, alias=None))
        return imports


@dataclasses.dataclass
class ArrayMarshmallowNode(CompositeMarshmallowNode):
    @property
    def _field_rhs(self):
        # wrap the child's RHS with list
        ret = self._first_child._field_rhs
        rw_arguments = []
        if self.stack.top.key != self.field_name:
            rw_arguments.append(f'data_key="{self.stack.top.key}"')
            rw_arguments.append(f'attribute="{self.stack.top.key}"')
        if rw_arguments:
            rw_arguments = ", " + ", ".join(rw_arguments)
        else:
            rw_arguments = ""
        return f"ma_fields.List({ret}{rw_arguments})"

    @property
    def field_imports(self) -> List[Import]:
        return self._first_child.field_imports

    @field_imports.setter
    def field_imports(self, imports):
        """Do not set imports as we generate the first child, not this node"""

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
        stack.push("model", schema.current_model)

        self.marshmallow_stack = [
            ObjectMarshmallowNode.from_stack(schema.schema, stack)
        ]

    def finish(self):
        super(PythonBuilder, self).finish()
        model_node = self.marshmallow_stack[0]

        # generate schema classes wherever they are not filled
        package_name = split_package_name(self.current_model.record_schema_class)

        generated_classes = defaultdict(list)
        generated_imports = defaultdict(set)

        model_node.mark_used()
        if model_node.generate:
            model_node.used = True

        context = {}
        known_classes = set()
        for fld in model_node.walk():
            fld.prepare(package_name, context)
            if hasattr(fld, "generate_schema_class"):
                package, class_name, generated_class = fld.generate_schema_class()
                if (package_name, class_name) in known_classes:
                    log.info(
                        f"Class renaming: have {package_name}.{class_name} twice, will use the first definition"
                    )
                else:
                    known_classes.add((package_name, class_name))
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
                if split_package_name(x.import_path)
                not in (
                    package_name,
                    # known prefixes
                    *BUILTIN_ALIASES,
                )
            ]

            self.process_template(
                python_path,
                self.template,
                current_package_name=package_name,
                imports=imports,
                generated_classes=generated_classes[package_name],
            )
        # super.finish not called as it is handled in the for loop above

    @process("**", condition=lambda current, stack: stack.schema_valid)
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
