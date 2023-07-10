from marshmallow import ValidationError

from oarepo_model_builder.validation.model_validation import model_validator


class InvalidModelException(Exception):
    pass


def flatten_errors(err_data, path):
    if isinstance(err_data, (list, tuple)):
        for err in err_data:
            yield from flatten_errors(err, path)
    elif isinstance(err_data, dict):
        for k, v in err_data.items():
            subpath = f"{path}.{k}" if path else k
            yield from flatten_errors(v, subpath)
    else:
        yield str(err_data), path


def validate_model(model):
    try:
        model.schema = model_validator.validate(model.schema)
        return True
    except ValidationError as e:
        msg = []
        for err, path in flatten_errors(e.messages_dict, ""):
            if path.endswith("._schema") and err == "Unknown field.":
                continue
            path = path.replace(".value.", ".")
            msg.append(f"{path}: {err}")
        msg = "\n    ".join(msg)
        raise InvalidModelException(f"Invalid model: \n    {msg}")
