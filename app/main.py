from fastapi import FastAPI
import uvicorn
from app.routes.login import router as login_router
from app.routes.documents import router as documents_router
from app.routes.recommendations import router as recommendations_router
from config import Config

app = FastAPI()
app.include_router(login_router, prefix=Config.PREFIX, tags=["login"])
app.include_router(documents_router, prefix=Config.PREFIX, tags=["documents"])
app.include_router(recommendations_router, prefix=Config.PREFIX, tags=["recommendations"])

@app.get("/")
def home():
    return {"message": "Welcome to Fasty-Recommender!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
