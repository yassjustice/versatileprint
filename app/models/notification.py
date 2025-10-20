"""
Notification model.
Handles in-app notifications for users.
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.models import BaseModel, Base


class Notification(Base, BaseModel):
    """Notification model."""
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    message = Column(Text, nullable=False)
    related_order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=True)
    is_read = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    notification_type = Column(String(50), default='info', comment='info, warning, error, success')
    
    # Relationships
    user = relationship('User', back_populates='notifications')
    order = relationship('Order', back_populates='notifications')
    
    def __repr__(self):
        return f'<Notification id={self.id} user_id={self.user_id} read={self.is_read}>'
    
    def to_dict(self, include_relations: bool = False) -> dict:
        """Convert to dictionary representation."""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message,
            'related_order_id': self.related_order_id,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'notification_type': self.notification_type
        }
        
        if include_relations and self.order:
            data['order'] = self.order.to_dict()
        
        return data
    
    def mark_as_read(self):
        """Mark notification as read."""
        self.is_read = True
        self.save()
    
    @classmethod
    def create_notification(cls, user_id: int, message: str, notification_type: str = 'info', 
                           related_order_id: int = None):
        """Create a new notification."""
        notification = cls(
            user_id=user_id,
            message=message,
            notification_type=notification_type,
            related_order_id=related_order_id
        )
        notification.save()
        return notification
    
    @classmethod
    def get_for_user(cls, user_id: int, unread_only: bool = False, limit: int = None, offset: int = 0):
        """Get notifications for a user."""
        session = cls.get_session()
        query = session.query(cls).filter_by(user_id=user_id)
        
        if unread_only:
            query = query.filter_by(is_read=False)
        
        query = query.order_by(cls.created_at.desc())
        
        if limit:
            query = query.limit(limit).offset(offset)
        
        return query.all()
    
    @classmethod
    def count_unread(cls, user_id: int) -> int:
        """Count unread notifications for user."""
        session = cls.get_session()
        return session.query(cls).filter_by(user_id=user_id, is_read=False).count()
    
    @classmethod
    def mark_all_read(cls, user_id: int):
        """Mark all notifications as read for user."""
        session = cls.get_session()
        session.query(cls).filter_by(user_id=user_id, is_read=False).update({'is_read': True})
        session.commit()
