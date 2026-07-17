import os

ALLOWED = {"config.json"}


def inline(user_path):
    return open(os.path.normpath(user_path))


def alias(user_path):
    safe_path = os.path.basename(user_path)
    return open(safe_path)


def guarded(path):
    if path not in ALLOWED:
        raise ValueError("invalid path")
    return open(path)


def literal():
    return open("static/config.json")
