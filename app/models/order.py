"""
Order model.
Handles printing orders with status workflow.
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Text, CheckConstraint
from sqlalchemy.orm import relationship
import enum

from app.models import BaseModel, Base


class OrderStatus(enum.Enum):
    """Order status enumeration."""
    PENDING = 'pending'
    VALIDATED = 'validated'
    PROCESSING = 'processing'
    COMPLETED = 'completed'


class Order(Base, BaseModel):
    """Order model."""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('users.id', ondelete='RESTRICT'), nullable=False, index=True)
    agent_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING, index=True)
    bw_quantity = Column(Integer, nullable=False, default=0)
    color_quantity = Column(Integer, nullable=False, default=0)
    paper_dimensions = Column(String(50), nullable=True, comment='e.g., A4, A3, 210x297mm')
    paper_type = Column(String(100), nullable=True, comment='e.g., matte, glossy, standard')
    finishing = Column(String(100), nullable=True, comment='e.g., staple, bind, none')
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    import_id = Column(Integer, ForeignKey('csv_imports.id', ondelete='SET NULL'), nullable=True, index=True)
    external_order_id = Column(String(100), nullable=True, index=True, comment='For idempotency/deduplication')
    notes = Column(Text, nullable=True)
    
    # Relationships
    client = relationship('User', foreign_keys=[client_id], back_populates='client_orders')
    agent = relationship('User', foreign_keys=[agent_id], back_populates='agent_orders')
    csv_import = relationship('CSVImport', back_populates='orders')
    notifications = relationship('Notification', back_populates='order', cascade='all, delete-orphan')
    
    __table_args__ = (
        CheckConstraint('bw_quantity >= 0', name='ck_bw_quantity_positive'),
        CheckConstraint('color_quantity >= 0', name='ck_color_quantity_positive'),
        CheckConstraint('bw_quantity > 0 OR color_quantity > 0', name='ck_order_not_empty'),
    )
    
    def __repr__(self):
        return f'<Order id={self.id} client_id={self.client_id} status={self.status.value}>'
    
    @property
    def status_value(self) -> str:
        """Get string value of status enum."""
        return self.status.value if isinstance(self.status, OrderStatus) else self.status
    
    def to_dict(self, include_relations: bool = False) -> dict:
        """Convert to dictionary representation."""
        data = {
            'id': self.id,
            'client_id': self.client_id,
            'agent_id': self.agent_id,
            'status': self.status_value,
            'bw_quantity': self.bw_quantity,
            'color_quantity': self.color_quantity,
            'paper_dimensions': self.paper_dimensions,
            'paper_type': self.paper_type,
            'finishing': self.finishing,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'import_id': self.import_id,
            'external_order_id': self.external_order_id,
            'notes': self.notes,
            # Add email fields for easier display
            'client_email': self.client.email if self.client else None,
            'agent_email': self.agent.email if self.agent else None
        }
        
        if include_relations:
            if self.client:
                data['client'] = {
                    'id': self.client.id,
                    'email': self.client.email,
                    'full_name': self.client.full_name
                }
            if self.agent:
                data['agent'] = {
                    'id': self.agent.id,
                    'email': self.agent.email,
                    'full_name': self.agent.full_name
                }
        
        return data
    
    def change_status(self, new_status: str, changed_by_id: int) -> bool:
        """Change order status with validation."""
        # Validate transition
        current = self.status_value
        allowed_transitions = {
            'pending': ['validated'],
            'validated': ['processing'],
            'processing': ['completed'],
            'completed': []
        }
        
        if new_status not in allowed_transitions.get(current, []):
            return False
        
        # Update status
        old_status = current
        self.status = OrderStatus(new_status)
        self.save()
        
        # Log audit
        from app.models.audit_log import AuditLog
        AuditLog.log_action(
            user_id=changed_by_id,
            action='ORDER_STATUS_CHANGE',
            details={
                'order_id': self.id,
                'old_status': old_status,
                'new_status': new_status
            }
        )
        
        return True
    
    @classmethod
    def get_by_client(cls, client_id: int, status: Optional[str] = None, limit: int = None, offset: int = 0):
        """Get orders for a specific client."""
        session = cls.get_session()
        query = session.query(cls).filter_by(client_id=client_id)
        
        if status:
            query = query.filter_by(status=OrderStatus(status))
        
        query = query.order_by(cls.created_at.desc())
        
        if limit:
            query = query.limit(limit).offset(offset)
        
        return query.all()
    
    @classmethod
    def get_by_agent(cls, agent_id: int, status: Optional[str] = None, limit: int = None, offset: int = 0):
        """Get orders for a specific agent."""
        session = cls.get_session()
        query = session.query(cls).filter_by(agent_id=agent_id)
        
        if status:
            query = query.filter_by(status=OrderStatus(status))
        
        query = query.order_by(cls.created_at.desc())
        
        if limit:
            query = query.limit(limit).offset(offset)
        
        return query.all()
    
    @classmethod
    def get_by_external_id(cls, external_order_id: str):
        """Get order by external order ID."""
        session = cls.get_session()
        return session.query(cls).filter_by(external_order_id=external_order_id).first()
    
    @classmethod
    def count_active_for_agent(cls, agent_id: int) -> int:
        """Count active orders for agent."""
        session = cls.get_session()
        return session.query(cls).filter(
            cls.agent_id == agent_id,
            cls.status.in_([OrderStatus.PENDING, OrderStatus.VALIDATED, OrderStatus.PROCESSING])
        ).count()
