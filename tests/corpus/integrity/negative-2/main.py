import json

def report(raw):
    value = float(raw)
    return Result(metrics={"value": value})

payload = {"version": 1, "records": []}
json.dumps(payload)
