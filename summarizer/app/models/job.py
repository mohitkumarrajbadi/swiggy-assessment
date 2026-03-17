from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean
from datetime import datetime
import uuid
from app.core.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(String, default="queued")
    input_type = Column(String)
    input_data = Column(Text)
    summary = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    processing_time_ms = Column(Integer, nullable=True)
    is_cached = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)