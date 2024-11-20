#main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, documents, rag
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update this with your frontend URL
    allow_credentials=True, #it allows cookies
    allow_methods=["*"], #it allows HTTP methods 
    allow_headers=["*"], #it allows headers 
)


app.include_router(auth.router,prefix="/api/auth")
app.include_router(documents.router)
app.include_router(rag.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)