import json

def classify(value):
    result = float(value)
    json.dumps({"result": result})
    return result
