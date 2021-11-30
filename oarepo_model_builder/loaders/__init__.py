try:
    import json5
except ImportError:
    import json as json5


def json_loader(file_path, schema):
    with open(file_path) as f:
        return json5.load(f)


json_loader.safe = True


def yaml_loader(file_path, schema):
    try:
        import yaml
    except ImportError:
        raise Exception('Loader for yaml not found. Please install pyyaml library to use yaml files')

    with open(file_path) as f:
        return yaml.full_load(f)


yaml_loader.safe = True


def python_loader(file_path, schema):
    with open(file_path) as f:
        code = f.read()
    # hope that user knows what he/she is doing
    gls = {}
    exec(code, gls)
    ret = {}
    for k, v in gls:
        try:
            json5.dumps(v)
        except:
            continue
        ret[k] = v
    return ret
