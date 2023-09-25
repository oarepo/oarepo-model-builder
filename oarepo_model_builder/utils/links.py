def url_prefix2link(url_prefix):
    ret = url_prefix.replace("<pid_value>", "{id}")
    if ret[-1] != "/":
        ret += "/"
    return ret
