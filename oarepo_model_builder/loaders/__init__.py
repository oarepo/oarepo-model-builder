from pathlib import Path

import json5
import yaml


def json_loader(path: Path):
    return json5.loads(path.read_text(encoding="utf-8"))


def yaml_loader(path: Path):
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)
