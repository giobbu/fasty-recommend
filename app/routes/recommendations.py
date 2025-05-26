from fastapi import APIRouter, HTTPException
from config import Config, KNN
from app.helpers.file_operations import load_from_db
from recommender import Recommender
from app.schemas.recommendations import RecommendationRequest, RecommendationResponse
from loguru import logger
import gc


router = APIRouter()


@router.post("/generate_recommendations", response_model=RecommendationResponse)
def create_recommendation(request: RecommendationRequest) -> RecommendationResponse:
    """
    Generate document recommendations based on input data.

    Args:
        request (RecommendationRequest): The incoming request with user data.

    Returns:
        RecommendationResponse: Response containing recommended documents.
    """
    try:
        input_data = request.data
        logger.debug("Received recommendation request with input data.")

        # Load documents from the database
        documents = load_from_db(Config.doc_db_path)
        if not documents:
            logger.warning("No documents found in the database.")
            raise HTTPException(status_code=500, detail="Document database is empty")

        # Initialize recommender
        recommender = Recommender(documents, k=KNN.k, metric=KNN.metric)

        # Generate recommendations
        recommended_docs = recommender.recommend(input_data)
        logger.debug(f"Generated recommendations: {recommended_docs}")

        if not recommended_docs:
            logger.info("No matching recommendations found.")
            raise HTTPException(status_code=404, detail="No recommendations found")

        return RecommendationResponse(
            message="Recommendation created successfully",
            data=recommended_docs
        )


    except Exception as e:
        logger.exception("Unexpected error during recommendation generation.")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        # Cleanup
        del recommender
        gc.collect()

