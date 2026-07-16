import pickle

secret_key = "secret-value-3"

def fetch(filename):
    pickle.load(filename)
    return open(filename)
