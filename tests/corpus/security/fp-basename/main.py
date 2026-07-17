import os

def load(slug):
    filename = os.path.basename(slug)
    return open(filename)
