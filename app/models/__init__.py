"""
Database models package.
Contains all SQLAlchemy model definitions.
"""
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.ext.declarative import declarative_base

# Create a single shared Base for all models
Base = declarative_base()

class BaseModel:
    """Base model with common functionality."""
    
    @classmethod
    def get_session(cls):
        """Get database session from app context."""
        from flask import current_app
        return current_app.db_session
    
    def save(self):
        """Save model instance to database."""
        session = self.get_session()
        session.add(self)
        session.commit()
        return self
    
    def delete(self):
        """Delete model instance from database."""
        session = self.get_session()
        session.delete(self)
        session.commit()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary representation."""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[column.name] = value
        return result
    
    @classmethod
    def get_by_id(cls, id: int):
        """Get model instance by ID."""
        session = cls.get_session()
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def get_all(cls, limit: Optional[int] = None, offset: int = 0):
        """Get all model instances with optional pagination."""
        session = cls.get_session()
        query = session.query(cls)
        if limit:
            query = query.limit(limit).offset(offset)
        return query.all()
    
    @classmethod
    def count(cls) -> int:
        """Get total count of model instances."""
        session = cls.get_session()
        return session.query(cls).count()

# Import all models to register them with SQLAlchemy
# Import order matters for relationship resolution
from app.models.user import Role, User
from app.models.quota import ClientQuota, QuotaTopup
from app.models.order import Order
from app.models.csv_import import CSVImport
from app.models.notification import Notification
from app.models.audit_log import AuditLog

__all__ = [
    'BaseModel',
    'Role',
    'User',
    'ClientQuota',
    'QuotaTopup',
    'Order',
    'CSVImport',
    'Notification',
    'AuditLog'
]
