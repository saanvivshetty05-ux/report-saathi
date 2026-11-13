from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from backend.app.models.system import SystemStatus
    Base.metadata.create_all(bind=engine)
    
    # Seed verification value if not already present
    db = SessionLocal()
    try:
        record = db.query(SystemStatus).filter(SystemStatus.key == "service_status").first()
        if not record:
            record = SystemStatus(
                key="service_status",
                value="ReportSaathi System v1.0 Operational"
            )
            db.add(record)
            db.commit()
    finally:
        db.close()
