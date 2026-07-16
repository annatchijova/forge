import os

secret = os.getenv("SECRET")

def read(filename):
    filename = os.path.normpath(filename)
    return open(filename)
