import json
import os
from loguru import logger
from fastapi import HTTPException

# Helper function to load a JSON file
def load_from_db(file_path: str):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# Helper function to save data to a JSON file
def save_to_db(file_path: str, data: dict):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save data: {str(e)}")

