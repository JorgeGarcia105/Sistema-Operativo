import sys
import os
import json

def resource_path(relative_path):
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_profiles_from_json(file_path):
    with open(file_path, 'r') as jsonfile:
        profiles = json.load(jsonfile)
    return profiles
