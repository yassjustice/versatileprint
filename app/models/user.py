"""
User and Role models.
Handles authentication, authorization, and user management.
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import bcrypt

from app.models import BaseModel, Base


class Role(Base, BaseModel):
    """Role model for RBAC."""
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    users = relationship('User', back_populates='role')
    
    def __repr__(self):
        return f'<Role {self.name}>'
    
    @classmethod
    def get_by_name(cls, name: str):
        """Get role by name."""
        session = cls.get_session()
        return session.query(cls).filter_by(name=name).first()
    
    @classmethod
    def get_client_role(cls):
        """Get Client role."""
        return cls.get_by_name('Client')
    
    @classmethod
    def get_agent_role(cls):
        """Get Agent role."""
        return cls.get_by_name('Agent')
    
    @classmethod
    def get_admin_role(cls):
        """Get Administrator role."""
        return cls.get_by_name('Administrator')


class User(Base, BaseModel, UserMixin):
    """User model with authentication support."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    role = relationship('Role', back_populates='users')
    client_quotas = relationship('ClientQuota', foreign_keys='ClientQuota.client_id', back_populates='client')
    topups_received = relationship('QuotaTopup', foreign_keys='QuotaTopup.client_id', back_populates='client')
    topups_given = relationship('QuotaTopup', foreign_keys='QuotaTopup.admin_id', back_populates='admin')
    client_orders = relationship('Order', foreign_keys='Order.client_id', back_populates='client')
    agent_orders = relationship('Order', foreign_keys='Order.agent_id', back_populates='agent')
    notifications = relationship('Notification', back_populates='user', cascade='all, delete-orphan')
    audit_logs = relationship('AuditLog', back_populates='user')
    csv_uploads = relationship('CSVImport', foreign_keys='CSVImport.uploaded_by', back_populates='uploader')
    csv_validations = relationship('CSVImport', foreign_keys='CSVImport.validated_by', back_populates='validator')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def set_password(self, password: str):
        """Hash and set user password."""
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )
    
    def update_last_login(self):
        """Update last login timestamp."""
        self.last_login = datetime.utcnow()
        self.save()
    
    @property
    def is_client(self) -> bool:
        """Check if user is a Client."""
        return self.role.name == 'Client'
    
    @property
    def is_agent(self) -> bool:
        """Check if user is an Agent."""
        return self.role.name == 'Agent'
    
    @property
    def is_admin(self) -> bool:
        """Check if user is an Administrator."""
        return self.role.name == 'Administrator'
    
    @property
    def role_name(self) -> str:
        """Get role name."""
        return self.role.name if self.role else None
    
    def to_dict(self, include_role=True) -> dict:
        """Convert user to dictionary representation."""
        data = {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        if include_role and self.role:
            data['role'] = {
                'id': self.role.id,
                'name': self.role.name
            }
            data['role_name'] = self.role.name  # Add role_name for convenience
        return data
    
    @classmethod
    def get_by_email(cls, email: str):
        """Get user by email."""
        session = cls.get_session()
        return session.query(cls).filter(cls.email == email).first()
    
    @classmethod
    def get_by_id(cls, user_id: int):
        """Get user by ID."""
        session = cls.get_session()
        return session.query(cls).filter(cls.id == user_id).first()
    
    @classmethod
    def get_by_role(cls, role_name: str, active_only: bool = True) -> List['User']:
        """Get all users with specific role."""
        session = cls.get_session()
        query = session.query(cls).join(Role).filter(Role.name == role_name)
        if active_only:
            query = query.filter(cls.is_active == True)
        return query.all()
    
    @classmethod
    def create_user(cls, email: str, password: str, full_name: str, role_name: str, is_active: bool = True):
        """Create a new user."""
        session = cls.get_session()
        
        # Get role
        role = Role.get_by_name(role_name)
        if not role:
            raise ValueError(f"Role '{role_name}' not found")
        
        # Check if email already exists
        if cls.get_by_email(email):
            raise ValueError(f"Email '{email}' already exists")
        
        # Create user
        user = cls(
            email=email,
            full_name=full_name,
            role_id=role.id,
            is_active=is_active
        )
        user.set_password(password)
        user.save()
        
        return user
    
    def get_active_orders_count(self) -> int:
        """Get count of active orders for agent."""
        if not self.is_agent:
            return 0
        
        from app.models.order import Order, OrderStatus
        session = self.get_session()
        
        return session.query(Order).filter(
            Order.agent_id == self.id,
            Order.status.in_([OrderStatus.PENDING, OrderStatus.VALIDATED, OrderStatus.PROCESSING])
        ).count()
    
    def can_accept_order(self, max_limit: int) -> bool:
        """Check if agent can accept new order."""
        if not self.is_agent:
            return False
        return self.get_active_orders_count() < max_limit
