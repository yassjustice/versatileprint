"""
Audit Log model.
Records all critical actions for compliance and debugging.
"""
from datetime import datetime
from typing import Optional, Any, Dict
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
import json as json_module

from app.models import BaseModel, Base


class AuditLog(Base, BaseModel):
    """Audit log model."""
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True, comment='e.g., ORDER_STATUS_CHANGE, CSV_VALIDATED, USER_LOGIN')
    details = Column(JSON, nullable=True, comment='Structured context')
    ip_address = Column(String(45), nullable=True, comment='IPv4 or IPv6')
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship('User', back_populates='audit_logs')
    
    def __repr__(self):
        return f'<AuditLog id={self.id} action={self.action}>'
    
    def to_dict(self, include_user: bool = False) -> dict:
        """Convert to dictionary representation."""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'details': self.details,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_user and self.user:
            data['user'] = {
                'id': self.user.id,
                'email': self.user.email,
                'full_name': self.user.full_name
            }
        
        return data
    
    @classmethod
    def log_action(cls, action: str, user_id: Optional[int] = None, details: Optional[Dict[str, Any]] = None,
                   ip_address: Optional[str] = None, user_agent: Optional[str] = None):
        """Create an audit log entry."""
        log = cls(
            user_id=user_id,
            action=action,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent
        )
        log.save()
        return log
    
    @classmethod
    def get_by_action(cls, action: str, limit: int = None, offset: int = 0):
        """Get audit logs by action type."""
        session = cls.get_session()
        query = session.query(cls).filter_by(action=action)
        query = query.order_by(cls.created_at.desc())
        
        if limit:
            query = query.limit(limit).offset(offset)
        
        return query.all()
    
    @classmethod
    def get_by_user(cls, user_id: int, limit: int = None, offset: int = 0):
        """Get audit logs for a specific user."""
        session = cls.get_session()
        query = session.query(cls).filter_by(user_id=user_id)
        query = query.order_by(cls.created_at.desc())
        
        if limit:
            query = query.limit(limit).offset(offset)
        
        return query.all()
    
    @classmethod
    def get_recent(cls, limit: int = 100):
        """Get recent audit logs."""
        session = cls.get_session()
        return session.query(cls).order_by(cls.created_at.desc()).limit(limit).all()
