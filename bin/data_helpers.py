import json

from box import Box


def read_json_as_dict(filename, raw=True):
    try:
        # Open the file and load the JSON data into a dictionary
        with open(filename, "r") as file:
            data = json.load(file)

        if not raw:
            return Box(data)
        # a Python dictionary
        return data
    except json.JSONDecodeError as e:
        print(f"Failed to read JSON file: {filename}. Error: {e}")
        return None
