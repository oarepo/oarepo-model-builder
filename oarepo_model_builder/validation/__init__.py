import copy
import importlib.resources
import json

import json5
import lazy_object_proxy
import pkg_resources
from jsonschema import Draft202012Validator
from jsonschema.exceptions import relevance

from oarepo_model_builder.utils.deepmerge import deepmerge


class InvalidModelException(Exception):
    pass


@lazy_object_proxy.Proxy
def model_json_schema():
    main_schema_path = importlib.resources.files("oarepo_model_builder.validation") / "schemas" / "common-schema.json5"
    schema = json5.loads(main_schema_path.read_text())
    for ep in pkg_resources.iter_entry_points(group="oarepo.model_schemas"):
        filename = ".".join(ep.attrs)
        data = pkg_resources.resource_string(ep.module_name, filename)
        data = json5.loads(data)
        schema["$defs"] = deepmerge(data, schema["$defs"], listmerge="extend")

    return schema


def validate_model(model, extra_validation_schemas=None):
    schema = copy.deepcopy(model_json_schema)
    if extra_validation_schemas:
        for e in extra_validation_schemas:
            schema["$defs"] = deepmerge(e, schema["$defs"], listmerge="extend")
    else:
        schema = model_json_schema

    data = json.loads(json.dumps(model.schema, default=lambda s: repr(s)))
    replace_array_keys(data)

    if "oarepo:model-validation" in data:
        schema["$defs"] = deepmerge(data.pop("oarepo:model-validation"), schema["$defs"], listmerge="extend")

    validator = Draft202012Validator(schema)

    errors = list(validator.iter_errors(data))

    if not errors:
        return True

    errors.sort(key=lambda e: (relevance(e), e.path))
    print("\nErrors (most relevant first):")
    for err in errors:
        print(f'    on path "/{"/".join(str(x) for x in err.path)}" : {err.message}')
        print(f'         schema path "/{"/".join(str(x) for x in err.schema_path)}"')
    raise InvalidModelException("Invalid model")


def replace_array_keys(schema):
    if isinstance(schema, (list, tuple)):
        for l in schema:
            replace_array_keys(l)
    elif isinstance(schema, dict):
        for k, v in list(schema.items()):
            replace_array_keys(v)
            if k.endswith("[]"):
                del schema[k]
                schema[k[:-2]] = v
