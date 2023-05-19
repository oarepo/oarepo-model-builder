try:
    import json5
except ImportError:
    import json as json5


def json_loader(
    file_path, schema, content=None  # NOSONAR schema kept for extensibility
):
    if content:
        return json5.loads(content)
    with open(file_path) as f:
        return json5.load(f)


def yaml_loader(
    file_path, schema, content=None  # NOSONAR schema kept for extensibility
):
    try:
        import yaml
    except ImportError:
        raise RuntimeError(
            "Loader for yaml not found. Please install pyyaml library to use yaml files"
        )

    if content:
        return yaml.full_load(content)

    with open(file_path) as f:
        return yaml.full_load(f)
