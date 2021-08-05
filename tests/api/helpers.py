
def navigate_json(src, *path):
    for p in path:
        src = src[p]

    return src


def _process_field(builder, src, path_list, config, outputs):
    for paths in path_list:
        builder.pre(navigate_json(src, *paths), config, ['properties'] + paths, outputs)
    for paths in reversed(path_list):
        builder.post(navigate_json(src, *paths), config, ['properties'] + paths, outputs)
