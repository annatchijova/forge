import json

def decide(raw):
    score = float(raw)
    json.dump({"score": score}, output)
    return score > 0.5
