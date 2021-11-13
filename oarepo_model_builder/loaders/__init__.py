try:
    import json5
except ImportError:
    import json as json5


def json_loader(file_path):
    with open(file_path) as f:
        return json5.load(f)


def yaml_loader(file_path):
    try:
        import yaml
    except ImportError:
        raise Exception('Loader for yaml not found. Please install pyyaml library to use yaml files')

    with open(file_path) as f:
        return yaml.full_load(f)
