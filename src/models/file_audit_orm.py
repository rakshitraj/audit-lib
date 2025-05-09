from sqlalchemy import Column, String, DateTime, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class FileAudit(Base):
    __tablename__ = 'file_audit'
    __table_args__ = (
        {'schema': 'data_store'}
    )
    
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(String)
    target_layer = Column(String)
    src_record_count = Column(Integer)
    target_record_count = Column(Integer)
    src_file = Column(String)
    target_file = Column(String)
    src_archive_file = Column(String)
    transaction_trail = Column(String)
    created_by = Column(String)
    status = Column(String)
    job_id = Column(String)
    run_id = Column(String)
    src_layer = Column(String)
    target_archive_file = Column(String)
    updated_by = Column(String)
    created_time = Column(DateTime)
    updated_time = Column(DateTime)