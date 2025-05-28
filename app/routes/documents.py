from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from app.helpers.file_operations import load_from_db, save_to_db
from config import Config
from app.schemas.documents import Document, AllDocuments
from app.helpers.login import get_current_active_user
from app.schemas.login import User
from loguru import logger
from recommender import Recommender
from config import KNN


router = APIRouter()


@router.get("/all_documents", response_model=AllDocuments)
def get_documents(current_user: User = Depends(get_current_active_user)):
    """
    Retrieve all documents from the database.
    
    Returns:
        JSONResponse: A response containing all documents.
    """
    try:
        documents = load_from_db(Config.doc_db_path)
        return {"message": "Documents retrieved successfully",
                "data": documents}
    except FileNotFoundError:
        raise HTTPException(status_code=404, 
                            detail="Document database not found")


@router.post("/add_document")
def add_document(document: Document):
    """
    Add a new document to the database.
    
    Args:
        document (dict): A dictionary containing the document data.
    
    Returns:
        JSONResponse: A response indicating success or failure.
    """
    
    input_data = document.data
    if not input_data:
        raise HTTPException(status_code=400, 
                            detail="No document data provided")
    if not isinstance(input_data, str):
        raise HTTPException(status_code=400, 
                            detail="Document data must be a string")
    if input_data in documents.values():
        raise HTTPException(status_code=400, 
                            detail="Document already exists")
    # Load existing documents from the database
    documents = load_from_db(Config.doc_db_path)
    if not documents:
            logger.warning("No documents found in the database.")
            raise HTTPException(status_code=500, detail="Document database is empty")

    # Add the new document to the existing documents
    documents[f"doc{str(len(documents) + 1)}"] = input_data
    
    save_to_db(Config.doc_db_path, documents)
    logger.debug("Document added successfully")

    # Overwrite the TF-IDF files if they exist
    recommender = Recommender(documents, k=KNN.k, metric=KNN.metric)
    recommender.create_tfidf_vectorizer()
    logger.debug("TF-IDF matrix and vectorizer created successfully")

    return {"message": "Document added successfully",
            "data": documents}