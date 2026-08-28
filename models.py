from sqlalchemy import Column, String, Integer, DateTime
from database import Base
import datetime

class Case(Base):
    __tablename__ = "cases"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    priority = Column(String)
    investigator = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(String, primary_key=True, index=True)
    case_id = Column(String, index=True)
    original_filename = Column(String)
    file_size = Column(Integer)
    sha256_hash = Column(String)
    custody_status = Column(String)
    uploaded_by = Column(String)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)