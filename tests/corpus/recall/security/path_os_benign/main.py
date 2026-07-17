import os


BASE = "/srv/artifacts"


def artifact_path(user_path):
    safe_path = os.path.normpath(user_path)
    return os.path.join(BASE, safe_path)
