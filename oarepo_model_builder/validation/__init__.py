import json

from oarepo_model_builder.utils.hyphen_munch import HyphenMunch, munch
from oarepo_model_builder.validation.model_validation import model_validator
from marshmallow import ValidationError


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
    data = json.loads(json.dumps(model.schema, default=lambda s: repr(s)))
    validator = model_validator.validator_class("root")()
    try:
        loaded_data = validator.dump(validator.load(data))
        model.schema = munch.munchify(loaded_data, HyphenMunch)
        return True
    except ValidationError as e:
        msg = []
        for err, path in flatten_errors(e.messages_dict, ""):
            msg.append(f"{path}: {err}")
        msg = "\n    ".join(msg)
        raise InvalidModelException(f"Invalid model: \n    {msg}")
