

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from app.db.models import Document, User
from app.core.config import settings
from fastapi.responses import JSONResponse

# Request body schema
class QueryRequest(BaseModel):
    query: str

router = APIRouter()

# Dependency imports for database and user
from app.db.base import get_db
from app.core.security import get_current_user

@router.post("/query")
async def query_documents(
    request: QueryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        # Fetch OpenAI API Key from settings
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not configured. Please set it in the .env file.")
        print("OPENAI_API_KEY loaded successfully")

        # Fetch documents for the current user
        documents = db.query(Document).filter(Document.user_id == current_user.id).all()
        texts = [doc.content for doc in documents]

        if not texts:
            return {"answer": "No documents found for the current user."}

        # Create embeddings and initialize FAISS vector store
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        vectorstore = FAISS.from_texts(texts, embeddings)

        # Initialize RetrievalQA
        qa_chain = RetrievalQA.from_chain_type(
            llm=OpenAI(openai_api_key=api_key),
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
        )

        # Perform the query and return the result
        result = qa_chain({"query": request.query})
        return {"answer": result["result"]}

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the query.")




