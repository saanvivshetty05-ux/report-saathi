"""
ReportSaathi Shared Python Pydantic Models
Source of truth: docs/06a-api-contract.md and shared/schemas/contract.json
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class RangeStatus(str, Enum):
    WITHIN_LAB_RANGE = "WITHIN_LAB_RANGE"
    OUTSIDE_LAB_RANGE = "OUTSIDE_LAB_RANGE"
    INDETERMINATE = "INDETERMINATE"


class DatabaseStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"


class HealthResponse(BaseModel):
    status: str = Field(..., description="Overall service status (healthy/degraded/unhealthy)")
    version: str = Field(..., description="Application semantic version")
    database_status: DatabaseStatus = Field(..., description="Database connection health")
    database_value: str = Field(..., description="Verification value read from database table")
    ocr_engine_available: bool = Field(..., description="Whether OCR binaries are available")
    supported_panels: List[str] = Field(default_factory=lambda: ["FBS", "PPBS", "HBA1C", "LIPID_PROFILE"])
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp")


class BiomarkerExtraction(BaseModel):
    parameter_code: str
    display_name_en: str
    display_name_hi: str
    observed_value: float
    unit: str
    lab_range_low: Optional[float] = None
    lab_range_high: Optional[float] = None
    status: RangeStatus
    ocr_confidence: float = Field(ge=0.0, le=1.0)


class ConfirmedParameter(BaseModel):
    parameter_code: str
    observed_value: float
    unit: str
    lab_range_low: Optional[float] = None
    lab_range_high: Optional[float] = None


class VerificationPayload(BaseModel):
    session_id: str
    language: Optional[str] = "en"
    confirmed_parameters: List[ConfirmedParameter]


class DoctorQuestion(BaseModel):
    id: str
    question_en: str
    question_hi: str


class DecodedBiomarker(BaseModel):
    parameter_code: str
    name_en: str
    name_hi: str
    observed_value: float
    unit: str
    lab_range: str
    status_tag: str
    plain_explanation_en: str
    plain_explanation_hi: str


class ReportSummaryLines(BaseModel):
    line_1: str
    line_2: str
    line_3: str


class WhatsAppPayload(BaseModel):
    encoded_url: str
    plain_text: str


class FinalReportCard(BaseModel):
    session_id: str
    summary: ReportSummaryLines
    decoded_biomarkers: List[DecodedBiomarker]
    doctor_questions: List[DoctorQuestion]
    statutory_disclaimer: str
    whatsapp_payload: WhatsAppPayload


class ErrorDetail(BaseModel):
    code: str
    message: str
    suggested_action: Optional[str] = None
    timestamp: str


class StandardError(BaseModel):
    success: bool = False
    error: ErrorDetail
