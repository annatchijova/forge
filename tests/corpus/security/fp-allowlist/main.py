ALLOWED = {"report.json"}

def load(name):
    if name not in ALLOWED:
        raise ValueError(name)
    return open(name)
