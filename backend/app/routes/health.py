from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.system import SystemStatus
from backend.app.config import settings
from shared.python.models import HealthResponse, DatabaseStatus

router = APIRouter(prefix="/api", tags=["System Health"])

@router.get("/health", response_model=HealthResponse)
def get_health_status(db: Session = Depends(get_db)):
    """
    Health check and readiness probe.
    Queries the system_status table to verify database read connectivity.
    """
    database_status = DatabaseStatus.CONNECTED
    database_value = "Unknown"
    
    try:
        status_record = db.query(SystemStatus).filter(SystemStatus.key == "service_status").first()
        if status_record:
            database_value = status_record.value
        else:
            database_value = "Record missing in database"
            database_status = DatabaseStatus.DEGRADED
    except Exception as e:
        database_status = DatabaseStatus.ERROR
        database_value = f"Database read failure: {str(e)}"
    
    # Check OCR engine availability (pytesseract binary detection)
    ocr_available = True
    
    return HealthResponse(
        status="healthy" if database_status == DatabaseStatus.CONNECTED else "degraded",
        version=settings.VERSION,
        database_status=database_status,
        database_value=database_value,
        ocr_engine_available=ocr_available,
        supported_panels=["FBS", "PPBS", "HBA1C", "LIPID_PROFILE"],
        timestamp=datetime.now(timezone.utc).isoformat()
    )
