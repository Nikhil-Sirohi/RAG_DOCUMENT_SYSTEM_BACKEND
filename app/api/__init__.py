# backend/app/api/__init__.py

from .auth import router as auth_router
from .documents import router as documents_router
from .rag import router as rag_router

__all__ = ['auth_router', 'documents_router', 'rag_router']