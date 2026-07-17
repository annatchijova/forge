import json
import pickle as p
import yaml


def parse(raw):
    return json.loads(raw), yaml.safe_load(raw), yaml.load(raw, Loader=yaml.SafeLoader), p
