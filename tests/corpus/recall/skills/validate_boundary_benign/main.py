ALLOWED = {"config.json"}


def handler(path):
    if path not in ALLOWED:
        raise ValueError("invalid path")
    return open(path).read()
