# backend/app/db/__init__.py

from .base import Base, get_db
from .models import User, Document

__all__ = ['Base', 'get_db', 'User', 'Document']