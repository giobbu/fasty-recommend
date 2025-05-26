from fastapi import APIRouter, HTTPException
from loguru import logger
from app.helpers.file_operations import load_from_db, save_to_db
from config import Config, KNN
from recommender import Recommender
from app.schemas.documents import Document, AllDocuments


router = APIRouter()


@router.get("/all_documents", response_model=AllDocuments)
def get_documents():
    """
    Retrieve all documents from the database.
    
    Returns:
        JSONResponse: A response containing all documents.
    """
    
    try:
        documents = load_from_db(Config.doc_db_path)
        logger.debug(f"Retrieved {len(documents)} documents from the database")
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
    logger.debug(f"Adding document: {input_data}")
    documents = load_from_db(Config.doc_db_path)
    logger.debug(f"Current number of documents: {len(documents)}")

    if not input_data:
        raise HTTPException(status_code=400, 
                            detail="No document data provided")
    if not isinstance(input_data, str):
        raise HTTPException(status_code=400, 
                            detail="Document data must be a string")
    if input_data in documents.values():
        raise HTTPException(status_code=400, 
                            detail="Document already exists")
    
    
    documents[f"doc{str(len(documents) + 1)}"] = input_data
    logger.debug(f"New number of documents: {len(documents)}")
    
    save_to_db(Config.doc_db_path, documents)
    logger.debug("Document added successfully")

    # Overwrite the TF-IDF files if they exist
    recommender = Recommender(documents, k=KNN.k, metric=KNN.metric)
    recommender.create_tfidf_vectorizer()
    logger.debug("TF-IDF matrix and vectorizer created successfully")

    return {"message": "Document added successfully",
            "data": documents}