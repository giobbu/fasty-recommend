from fastapi import FastAPI
import uvicorn
from app.routes.descriptions import router as descriptions_router
from app.routes.recommendations import router as recommendations_router

app = FastAPI()
app.include_router(descriptions_router, prefix="/api", tags=["descriptions"])
app.include_router(recommendations_router, prefix="/api", tags=["recommendations"])

@app.get("/")
def home():
    return {"message": "Welcome to Fasty-Recommender!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
