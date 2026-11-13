import unittest
from pydantic import ValidationError
from shared.python.models import (
    HealthResponse,
    DatabaseStatus,
    RangeStatus,
    BiomarkerExtraction,
    VerificationPayload,
    ConfirmedParameter,
    FinalReportCard,
    ReportSummaryLines,
    DoctorQuestion,
    DecodedBiomarker,
    WhatsAppPayload
)

class TestContractSchemas(unittest.TestCase):
    def test_health_response_schema_valid(self):
        payload = {
            "status": "healthy",
            "version": "1.0.0",
            "database_status": "connected",
            "database_value": "ReportSaathi System v1.0 Operational",
            "ocr_engine_available": True,
            "supported_panels": ["FBS", "HBA1C"],
            "timestamp": "2026-11-13T08:30:00Z"
        }
        res = HealthResponse(**payload)
        self.assertEqual(res.status, "healthy")
        self.assertEqual(res.database_status, DatabaseStatus.CONNECTED)
        self.assertEqual(res.database_value, "ReportSaathi System v1.0 Operational")

    def test_health_response_schema_invalid(self):
        # Missing required fields
        with self.assertRaises(ValidationError):
            HealthResponse(status="healthy")

    def test_verification_payload_schema(self):
        payload = {
            "session_id": "test-session-123",
            "language": "en",
            "confirmed_parameters": [
                {
                    "parameter_code": "FBS",
                    "observed_value": 114.0,
                    "unit": "mg/dL",
                    "lab_range_low": 70.0,
                    "lab_range_high": 99.0
                }
            ]
        }
        v = VerificationPayload(**payload)
        self.assertEqual(v.session_id, "test-session-123")
        self.assertEqual(len(v.confirmed_parameters), 1)
        self.assertEqual(v.confirmed_parameters[0].parameter_code, "FBS")

    def test_final_report_card_schema(self):
        card = FinalReportCard(
            session_id="session-456",
            summary=ReportSummaryLines(
                line_1="Tested Fasting Sugar",
                line_2="Fasting Sugar is outside lab range",
                line_3="Consult your doctor this week"
            ),
            decoded_biomarkers=[
                DecodedBiomarker(
                    parameter_code="FBS",
                    name_en="Fasting Blood Sugar",
                    name_hi="फास्टिंग ब्लड शुगर",
                    observed_value=114.0,
                    unit="mg/dL",
                    lab_range="70 - 99 mg/dL",
                    status_tag="Outside Lab Printed Range",
                    plain_explanation_en="Measures sugar after fasting",
                    plain_explanation_hi="सुबह का ब्लड शुगर"
                )
            ],
            doctor_questions=[
                DoctorQuestion(
                    id="Q-FBS-01",
                    question_en="Should I adjust my diet?",
                    question_hi="क्या मुझे आहार बदलना चाहिए?"
                )
            ],
            statutory_disclaimer="Educational health literacy aid only.",
            whatsapp_payload=WhatsAppPayload(
                encoded_url="https://wa.me/?text=Report",
                plain_text="Report Summary"
            )
        )
        self.assertEqual(card.session_id, "session-456")
        self.assertEqual(len(card.decoded_biomarkers), 1)

if __name__ == "__main__":
    unittest.main()
