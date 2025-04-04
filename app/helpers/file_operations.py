import json
import os
from loguru import logger
from fastapi import HTTPException

# Helper function to load a JSON file
def load_json(file_path: str):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# Helper function to save data to a JSON file
def save_json(file_path: str, data: dict):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save data: {str(e)}")

# Helper function to validate inputs
def validate_input(value, expected_type, field_name):
    if not value:
        raise HTTPException(status_code=400, detail=f"No {field_name} provided")
    if not isinstance(value, expected_type):
        raise HTTPException(status_code=400, detail=f"{field_name} must be a {expected_type.__name__}")

def delete_tfidf_files(path_1: str, path_2: str):
    """
    Delete the TF-IDF files if they exist.
    """
    if os.path.isfile(path_1) or os.path.isfile(path_2):
        os.remove(path_1)
        logger.debug(f"Deleted {path_1}")
        os.remove(path_2)
        logger.debug(f"Deleted {path_2}")

