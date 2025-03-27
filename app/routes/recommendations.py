from fastapi import APIRouter, HTTPException
from collections import defaultdict
from app.config import Config
from app.helpers.file_operations import load_json, validate_input
from app.recommender import Recommender

router = APIRouter()

@router.post("/recommendations")
def create_recommendation(recommendation: dict):
    """
    Create a new recommendation.
    """
    try:
        validate_input(recommendation, dict, "recommendation")
        data = recommendation.get("data")
        validate_input(data, list, "data")
        documents = load_json(Config.doc_db_path)
        lst_documents = [doc for doc in documents.values()]
        recommender = Recommender(lst_documents)
        recommendations = recommender.recommend(data)
        document_to_recommend = {doc: description for doc, description in documents.items() if description in recommendations}
        return {"message": "Recommendation created successfully", 
                "data": document_to_recommend}
    except Exception as e:
        # General exceptions, not handled by HTTPException
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")