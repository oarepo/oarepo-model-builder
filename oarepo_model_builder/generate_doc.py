import marshmallow.fields as fields

from oarepo_model_builder.datatypes import datatypes
from oarepo_model_builder.datatypes.containers.object import (
    FieldSchema,
    ObjectPropertiesField,
)
from oarepo_model_builder.validation.extensibility import ExtensibleSchema
from oarepo_model_builder.validation.model_validation import ModelFileSchema


def escape(x):
    return x.replace("<", "&lt;").replace(">", "&gt;")


def generate_doc(outfile):
    complete_model_schema = ExtensibleSchema("model_file", ModelFileSchema)
    schemas = {}
    collect_schema(type(complete_model_schema()), schemas)

    for schema_name, schema in schemas.items():
        print(schema_name)
        for fld_name, fld in sorted(schema["fields"].items()):
            print("    ", fld_name, fld)

    with open(outfile, "w") as f:
        for schema_class, schema in schemas.items():
            print(f"## [{schema_class.__name__}](#{schema_class.__name__})", file=f)
            if schema_class.__doc__:
                print(f"{schema_class.__doc__}", file=f)
            print(file=f)
            print("| property | type | documentation |", file=f)
            print("| --- | --- | --- |", file=f)
            for fld_name, fld in sorted(schema["fields"].items()):
                if "ref" in fld:
                    fld_col = f'[{fld["ref"].__name__}](#{fld["ref"].__name__})'
                else:
                    fld_col = fld["type"]
                if "array" in fld:
                    fld_col = f"Array of {fld_col}"
                print(f'| {fld_name} | {fld_col} | {fld.get("doc") } |', file=f)


def collect_schema(schema, schemas):
    if schema in schemas:
        return
    flds = {}
    schemas[schema] = {"fields": flds, "schema": schema}
    if schema is FieldSchema:
        for datatype_name, datatype_class in datatypes.datatype_map.items():
            validator = type(datatype_class.validator())
            collect_schema(validator, schemas)
            flds[f"_{datatype_name}_"] = {
                "type": "Nested",
                "ref": validator,
                "doc": "",
            }
    else:
        for fld_name, fld in schema._declared_fields.items():
            flds[fld.attribute or fld_name] = {
                **collect_field(fld_name, fld, schemas),
                "doc": escape(fld.metadata.get("doc") or ""),
            }


def collect_field(fld_name, fld, schemas):
    if isinstance(fld, fields.Nested):
        subschema = type(fld.schema)
        collect_schema(subschema, schemas)
        return {"type": type(fld).__name__, "ref": subschema}
    elif isinstance(fld, fields.List):
        return {**collect_field(fld_name, fld.inner, schemas), "array": True}
    elif isinstance(fld, ObjectPropertiesField):
        if ObjectPropertiesField not in schemas:
            schemas[ObjectPropertiesField] = {
                "fields": {
                    "*": collect_field(fld_name, fld.value_field, schemas),
                },
                "schema": ObjectPropertiesField,
            }
        return {"type": type(fld).__name__, "ref": ObjectPropertiesField}
    else:
        return {"doc": fld.metadata.get("doc") or fld_name, "type": type(fld).__name__}


if __name__ == "__main__":
    generate_doc("SCHEMA.md")
