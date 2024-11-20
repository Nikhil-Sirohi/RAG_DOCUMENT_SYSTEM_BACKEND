#app/services/rag_service.py


from sqlalchemy.orm import Session
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from app.db.models import Document

async def query_documents(query: str, db: Session, current_user: str):
    # Retrieve user's documents
    documents = db.query(Document).filter(Document.user_id == current_user).all()
    
    # Create a list of document contents
    texts = [doc.content for doc in documents]

    # Create embeddings
    embeddings = OpenAIEmbeddings()
    
    # Create vector store
    vectorstore = FAISS.from_texts(texts, embeddings)

    # Create retrieval chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    # Query the documents
    result = qa_chain({"query": query})

    return {"answer": result['result']}