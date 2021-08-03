
def navigate_json(src, *path):
    for p in path:
        src = src[p]

    return src
