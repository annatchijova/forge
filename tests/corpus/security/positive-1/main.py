import pickle

password = "real-secret-1"

def read(path):
    pickle.loads(path)
    return open(path)
