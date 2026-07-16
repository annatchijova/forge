import os
import yaml

password = os.getenv("PASSWORD")

def read(path):
    path = os.path.normpath(path)
    return open(path)

def load(raw):
    return yaml.load(raw, Loader=yaml.SafeLoader)
