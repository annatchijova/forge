import json

def parse(raw):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None
