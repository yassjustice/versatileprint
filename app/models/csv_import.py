"""
CSV Import model.
Handles bulk order imports via CSV files.
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
import enum

from app.models import BaseModel, Base


class CSVImportStatus(enum.Enum):
    """CSV import status enumeration."""
    PENDING_VALIDATION = 'pending_validation'
    VALIDATED = 'validated'
    REJECTED = 'rejected'


class CSVImport(Base, BaseModel):
    """CSV import model."""
    __tablename__ = 'csv_imports'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uploaded_by = Column(Integer, ForeignKey('users.id', ondelete='RESTRICT'), nullable=False, index=True)
    original_filename = Column(String(255), nullable=False)
    stored_filepath = Column(String(500), nullable=False)
    status = Column(Enum(CSVImportStatus), nullable=False, default=CSVImportStatus.PENDING_VALIDATION, index=True)
    uploaded_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    validated_by = Column(Integer, ForeignKey('users.id', ondelete='RESTRICT'), nullable=True, index=True)
    validated_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True, comment='Admin review notes')
    row_count = Column(Integer, default=0, comment='Total rows in CSV')
    valid_rows = Column(Integer, default=0, comment='Valid rows after validation')
    error_rows = Column(Integer, default=0, comment='Rows with errors')
    
    # Relationships
    uploader = relationship('User', foreign_keys=[uploaded_by], back_populates='csv_uploads')
    validator = relationship('User', foreign_keys=[validated_by], back_populates='csv_validations')
    orders = relationship('Order', back_populates='csv_import')
    
    def __repr__(self):
        return f'<CSVImport id={self.id} file={self.original_filename} status={self.status.value}>'
    
    @property
    def status_value(self) -> str:
        """Get string value of status enum."""
        return self.status.value if isinstance(self.status, CSVImportStatus) else self.status
    
    def to_dict(self, include_relations: bool = False) -> dict:
        """Convert to dictionary representation."""
        data = {
            'id': self.id,
            'uploaded_by': self.uploaded_by,
            'original_filename': self.original_filename,
            'stored_filepath': self.stored_filepath,
            'status': self.status_value,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'validated_by': self.validated_by,
            'validated_at': self.validated_at.isoformat() if self.validated_at else None,
            'notes': self.notes,
            'row_count': self.row_count,
            'valid_rows': self.valid_rows,
            'error_rows': self.error_rows
        }
        
        if include_relations:
            if self.uploader:
                data['uploader'] = {
                    'id': self.uploader.id,
                    'email': self.uploader.email,
                    'full_name': self.uploader.full_name
                }
            if self.validator:
                data['validator'] = {
                    'id': self.validator.id,
                    'email': self.validator.email,
                    'full_name': self.validator.full_name
                }
        
        return data
    
    def mark_validated(self, validated_by_id: int, valid_count: int, error_count: int, notes: str = None):
        """Mark import as validated."""
        self.status = CSVImportStatus.VALIDATED
        self.validated_by = validated_by_id
        self.validated_at = datetime.utcnow()
        self.valid_rows = valid_count
        self.error_rows = error_count
        if notes:
            self.notes = notes
        self.save()
    
    def mark_rejected(self, validated_by_id: int, notes: str):
        """Mark import as rejected."""
        self.status = CSVImportStatus.REJECTED
        self.validated_by = validated_by_id
        self.validated_at = datetime.utcnow()
        self.notes = notes
        self.save()
    
    @classmethod
    def get_pending(cls, limit: int = None):
        """Get all pending CSV imports."""
        session = cls.get_session()
        query = session.query(cls).filter_by(status=CSVImportStatus.PENDING_VALIDATION)
        query = query.order_by(cls.uploaded_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @classmethod
    def get_by_uploader(cls, uploader_id: int, limit: int = None):
        """Get CSV imports by uploader."""
        session = cls.get_session()
        query = session.query(cls).filter_by(uploaded_by=uploader_id)
        query = query.order_by(cls.uploaded_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
