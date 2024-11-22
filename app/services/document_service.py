#app/services/document_service.py
import os
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.db.models import Document, User
from unstructured.partition.auto import partition

async def process_document(file: UploadFile, db: Session, current_user: User):
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            if not content:
                raise HTTPException(status_code=400, detail="Uploaded file is empty")
            buffer.write(content)

        elements = partition(file_path)
        text_content = "\n".join([str(element) for element in elements])

        document = Document(
            filename=file.filename, content=text_content, user_id=current_user.id
        )
        db.add(document)
        db.commit()
        db.refresh(document)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
    return {"message": "Document processed successfully", "document_id": document.id}

