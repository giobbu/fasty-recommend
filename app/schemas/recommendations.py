from pydantic import BaseModel

class RecommendationRequest(BaseModel):
    data: list

class RecommendationResponse(BaseModel):
    message: str
    data: dict