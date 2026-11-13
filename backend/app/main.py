from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.database import init_db
from backend.app.routes import health

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables and seed operational verification status
    init_db()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Stateless plain-language diagnostic report companion API",
    lifespan=lifespan
)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(health.router)

@app.get("/")
def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs_url": "/docs"
    }
