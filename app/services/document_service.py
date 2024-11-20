#app/services/document_service.py


import os
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.db.models import Document
from unstructured.partition.auto import partition

async def process_document(file: UploadFile, db: Session, current_user: str):
    # Save the file
    file_path = "uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # Parse the document using unstructured
    elements = partition(file_path)

    # Extract text content
    text_content = "\n".join([str(element) for element in elements])

    # Save document info to database
    document = Document(
        filename=file.filename,
        content=text_content,
        user_id=current_user
    )
    db.add(document)
    db.commit()

    # Clean up the file
    os.remove(file_path)

    return {"message": "Document processed successfully"}