import json
import codecs


def load_json_str(json_str):
    json_data = json.loads(json_str)
    return json_data


def load_json_file(json_file):
    with codecs.open(json_file, 'r', 'utf-8') as f:
        json_data = json.load(f)
        return json_data
