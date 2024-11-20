#app/api/documents.py


from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.document_service import process_document
from app.core.security import get_current_user

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return await process_document(file, db, current_user)



@router.get("/documents")
async def get_documents(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    documents = db.query(Document).filter(Document.user_id == current_user).all()
    return documents



@router.get("/documents/{document_id}")
async def get_document(document_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    document = db.query(Document).filter(Document.id == document_id, Document.user_id == current_user).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document