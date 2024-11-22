#app/api/rag.py


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.rag_service import query_documents
from app.core.security import get_current_user
from app.db.models import User


router = APIRouter()

@router.post("/query")
async def query(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await query_documents(query, db, current_user)


