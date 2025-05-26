from fastapi import APIRouter, HTTPException
from app.config import Config
from app.helpers.file_operations import load_json
from app.recommender import Recommender
from app.schemas.recommendations import RecommendationRequest, RecommendationResponse

router = APIRouter()


@router.post("/generate_recommendations", response_model=RecommendationResponse)
def create_recommendation(request: RecommendationRequest):
    """
    Generate document recommendations based on input data.

    Args:
        request (RecommendationRequest): The incoming request with data.

    Returns:
        dict: Recommended documents.
    """
    try:
        input_data = request.data

        # Load and prepare documents
        all_documents = load_json(Config.doc_db_path)
        document_list = list(all_documents.values())

        # Generate recommendations
        recommender = Recommender(document_list)
        recommended_descriptions = recommender.recommend(input_data)

        # Map descriptions back to document IDs
        recommended_docs = [
                            {doc_id: desc}
                            for doc_id, desc in all_documents.items() if desc in recommended_descriptions
                                ]

        if not recommended_docs:
            raise HTTPException(status_code=404, detail="No recommendations found")

        return {
            "message": "Recommendation created successfully",
            "data": recommended_docs
        }

    except HTTPException:
        raise  # Re-raise known HTTP errors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

