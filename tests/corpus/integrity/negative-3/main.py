import json

def emit(raw):
    profile = {"latency": float(raw)}
    return Result(profile=profile)

data = {"benchmark_schema_version": "1.0"}
json.dump(data, output)
