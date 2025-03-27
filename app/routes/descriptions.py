from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.helpers.file_operations import load_json, save_json, validate_input
from app.config import Config

router = APIRouter()

@router.get("/descriptions")
def get_descriptions():
    """
    Get a list of descriptions.
    """
    documents = load_json(Config.doc_db_path)
    return JSONResponse(content=documents)

@router.post("/add_description")
def add_description(description: dict):
    """
    Add a new description.
    """
    data = description.get("data")
    validate_input(data, dict, "data")
    documents = load_json(Config.doc_db_path)

    if data in documents.values():
        raise HTTPException(status_code=400, detail="Document already exists")

    documents[str(len(documents) + 1)] = data
    save_json(Config.doc_db_path, documents)
    return JSONResponse(status_code=201, content={"message": "Description added successfully", "data": data})