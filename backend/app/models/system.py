from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime, timezone
from backend.app.database import Base

class SystemStatus(Base):
    __tablename__ = "system_status"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), unique=True, index=True, nullable=False)
    value = Column(String(255), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
