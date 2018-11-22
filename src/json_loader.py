import json
import codecs
import os


def load_json_file(json_file, mod_time=0):
    if mod_time != 0 & mod_time == os.path.getmtime(json_file):
        return -1
    with codecs.open(json_file, 'r', 'utf-8') as f:
        json_data = json.load(f)
        return json_data
