from fastapi import FastAPI
import uvicorn
from app.routes.login import router as login_router
from app.routes.documents import router as documents_router
from app.routes.recommendations import router as recommendations_router

app = FastAPI()
app.include_router(login_router, prefix="/api", tags=["login"])
app.include_router(documents_router, prefix="/api", tags=["documents"])
app.include_router(recommendations_router, prefix="/api", tags=["recommendations"])

@app.get("/")
def home():
    return {"message": "Welcome to Fasty-Recommender!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
