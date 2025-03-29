from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.helpers.file_operations import load_json, save_json, validate_input, delete_tfidf_files
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
    validate_input(data, str, "data")
    documents = load_json(Config.doc_db_path)
    if data in documents.values():
        raise HTTPException(status_code=400, 
                            detail="Document already exists")
    documents[f"doc{str(len(documents) + 1)}"] = data
    save_json(Config.doc_db_path, documents)
    delete_tfidf_files(Config.doc_word_path, 
                    Config.vectorizer_path)
    return JSONResponse(status_code=201, content={"message": "Description added successfully", "data": data})