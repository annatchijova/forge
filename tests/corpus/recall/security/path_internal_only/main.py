def _read(path):
    return open(path).read()


def read_config():
    return _read("config.json")
