import json

def report(raw):
    telemetry = {"score": float(raw)}
    return Result(telemetry=telemetry)

json.dump({"schema_version": "1.0", "items": []}, output)
