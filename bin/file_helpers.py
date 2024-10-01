import glob
import os


def strip_extension(file_name):
    """Strip .json extension from the file name"""
    return os.path.splitext(file_name)[0]


def get_json_files(directory):
    # Get all .json files in the directory
    return glob.glob(os.path.join(directory, "*.json"))
