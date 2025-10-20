"""
Quota and Topup models.
Handles monthly quota limits and top-up transactions.
"""
from datetime import datetime, date
from typing import Optional, Tuple
from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, Text, Boolean, CheckConstraint
from sqlalchemy.orm import relationship

from app.models import BaseModel, Base


class ClientQuota(Base, BaseModel):
    """Client monthly quota model."""
    __tablename__ = 'client_quotas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    month = Column(Date, nullable=False, comment='Normalized as YYYY-MM-01')
    bw_limit = Column(Integer, nullable=False, default=3000)
    color_limit = Column(Integer, nullable=False, default=2000)
    bw_used = Column(Integer, nullable=False, default=0)
    color_used = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    bw_alert_sent = Column(Boolean, nullable=False, default=False, comment='Track if 80% alert sent for B&W')
    color_alert_sent = Column(Boolean, nullable=False, default=False, comment='Track if 80% alert sent for Color')
    
    # Relationships
    client = relationship('User', foreign_keys=[client_id], back_populates='client_quotas')
    
    __table_args__ = (
        CheckConstraint('bw_limit >= 0', name='ck_bw_limit_positive'),
        CheckConstraint('color_limit >= 0', name='ck_color_limit_positive'),
        CheckConstraint('bw_used >= 0', name='ck_bw_used_positive'),
        CheckConstraint('color_used >= 0', name='ck_color_used_positive'),
    )
    
    def __repr__(self):
        return f'<ClientQuota client_id={self.client_id} month={self.month}>'
    
    def get_available_bw(self, include_topups: bool = True) -> int:
        """Calculate available B&W quota."""
        total_limit = self.bw_limit
        
        if include_topups:
            topups = QuotaTopup.get_topups_for_month(self.client_id, self.month)
            total_limit += sum(t.bw_added for t in topups)
        
        return max(0, total_limit - self.bw_used)
    
    def get_available_color(self, include_topups: bool = True) -> int:
        """Calculate available Color quota."""
        total_limit = self.color_limit
        
        if include_topups:
            topups = QuotaTopup.get_topups_for_month(self.client_id, self.month)
            total_limit += sum(t.color_added for t in topups)
        
        return max(0, total_limit - self.color_used)
    
    def get_total_limits(self) -> Tuple[int, int]:
        """Get total limits including top-ups (bw, color)."""
        topups = QuotaTopup.get_topups_for_month(self.client_id, self.month)
        total_bw = self.bw_limit + sum(t.bw_added for t in topups)
        total_color = self.color_limit + sum(t.color_added for t in topups)
        return total_bw, total_color
    
    def check_usage_threshold(self, threshold: float = 0.8) -> dict:
        """Check if usage exceeds threshold (default 80%)."""
        total_bw, total_color = self.get_total_limits()
        
        bw_percentage = self.bw_used / total_bw if total_bw > 0 else 0
        color_percentage = self.color_used / total_color if total_color > 0 else 0
        
        return {
            'bw_exceeded': bw_percentage >= threshold and not self.bw_alert_sent,
            'color_exceeded': color_percentage >= threshold and not self.color_alert_sent,
            'bw_percentage': bw_percentage,
            'color_percentage': color_percentage
        }
    
    def mark_alert_sent(self, alert_type: str):
        """Mark alert as sent to prevent duplicates."""
        if alert_type == 'bw':
            self.bw_alert_sent = True
        elif alert_type == 'color':
            self.color_alert_sent = True
        self.save()
    
    def can_fulfill(self, bw_quantity: int, color_quantity: int) -> Tuple[bool, str]:
        """Check if quota can fulfill order quantities."""
        available_bw = self.get_available_bw()
        available_color = self.get_available_color()
        
        if bw_quantity > available_bw:
            return False, f'Insufficient B&W quota. Available: {available_bw}, Requested: {bw_quantity}'
        
        if color_quantity > available_color:
            return False, f'Insufficient Color quota. Available: {available_color}, Requested: {color_quantity}'
        
        return True, 'OK'
    
    def deduct_quota(self, bw_quantity: int, color_quantity: int):
        """Deduct quantities from quota (with transaction lock)."""
        self.bw_used += bw_quantity
        self.color_used += color_quantity
        self.save()
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        total_bw, total_color = self.get_total_limits()
        
        return {
            'id': self.id,
            'client_id': self.client_id,
            'month': self.month.isoformat(),
            'bw_limit': self.bw_limit,
            'color_limit': self.color_limit,
            'bw_used': self.bw_used,
            'color_used': self.color_used,
            'bw_available': self.get_available_bw(),
            'color_available': self.get_available_color(),
            'total_bw_limit': total_bw,
            'total_color_limit': total_color,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_or_create(cls, client_id: int, month: date, bw_limit: int = 3000, color_limit: int = 2000):
        """Get existing quota or create new one for month."""
        session = cls.get_session()
        
        # Normalize month to first day
        normalized_month = month.replace(day=1)
        
        quota = session.query(cls).filter_by(
            client_id=client_id,
            month=normalized_month
        ).first()
        
        if not quota:
            quota = cls(
                client_id=client_id,
                month=normalized_month,
                bw_limit=bw_limit,
                color_limit=color_limit,
                bw_used=0,
                color_used=0
            )
            quota.save()
        
        return quota
    
    @classmethod
    def get_for_client_month(cls, client_id: int, month: date):
        """Get quota for specific client and month."""
        session = cls.get_session()
        normalized_month = month.replace(day=1)
        return session.query(cls).filter_by(
            client_id=client_id,
            month=normalized_month
        ).first()


class QuotaTopup(Base, BaseModel):
    """Quota top-up transaction model."""
    __tablename__ = 'quota_topups'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    admin_id = Column(Integer, ForeignKey('users.id', ondelete='RESTRICT'), nullable=False, index=True)
    bw_added = Column(Integer, nullable=False, default=0)
    color_added = Column(Integer, nullable=False, default=0)
    transaction_date = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    client = relationship('User', foreign_keys=[client_id], back_populates='topups_received')
    admin = relationship('User', foreign_keys=[admin_id], back_populates='topups_given')
    
    __table_args__ = (
        CheckConstraint('bw_added >= 0', name='ck_bw_added_positive'),
        CheckConstraint('color_added >= 0', name='ck_color_added_positive'),
        CheckConstraint('bw_added > 0 OR color_added > 0', name='ck_topup_not_zero'),
    )
    
    def __repr__(self):
        return f'<QuotaTopup client_id={self.client_id} bw={self.bw_added} color={self.color_added}>'
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'admin_id': self.admin_id,
            'bw_added': self.bw_added,
            'color_added': self.color_added,
            'transaction_date': self.transaction_date.isoformat() if self.transaction_date else None,
            'notes': self.notes
        }
    
    @classmethod
    def get_topups_for_month(cls, client_id: int, month: date):
        """Get all top-ups for a specific client and month."""
        session = cls.get_session()
        
        # Calculate month boundaries
        start_date = month.replace(day=1)
        if month.month == 12:
            end_date = date(month.year + 1, 1, 1)
        else:
            end_date = date(month.year, month.month + 1, 1)
        
        return session.query(cls).filter(
            cls.client_id == client_id,
            cls.transaction_date >= start_date,
            cls.transaction_date < end_date
        ).all()
    
    @classmethod
    def create_topup(cls, client_id: int, admin_id: int, bw_added: int = 0, color_added: int = 0, notes: str = None):
        """Create a new top-up transaction."""
        if bw_added <= 0 and color_added <= 0:
            raise ValueError('Top-up must add at least one type of quota')
        
        topup = cls(
            client_id=client_id,
            admin_id=admin_id,
            bw_added=bw_added,
            color_added=color_added,
            notes=notes
        )
        topup.save()
        
        return topup
