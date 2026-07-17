import os

def load(name):
    handle = open(name)
    name = os.path.basename(name)
    return handle
