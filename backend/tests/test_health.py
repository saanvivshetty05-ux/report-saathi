import unittest
from backend.app.database import SessionLocal, init_db
from backend.app.routes.health import get_health_status
from shared.python.models import HealthResponse, DatabaseStatus

class TestHealthEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def setUp(self):
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_health_endpoint_reads_from_database(self):
        """
        Contract & Smoke Test:
        Verifies that GET /api/health queries the operational database,
        retrieves the seeded 'service_status' key, and returns
        the verified value adhering to the HealthResponse contract schema.
        """
        response = get_health_status(db=self.db)
        
        # Verify schema validity
        self.assertIsInstance(response, HealthResponse)
        
        # Verify database read value
        self.assertEqual(response.status, "healthy")
        self.assertEqual(response.database_status, DatabaseStatus.CONNECTED)
        self.assertEqual(response.database_value, "ReportSaathi System v1.0 Operational")
        self.assertTrue(response.ocr_engine_available)
        self.assertIn("FBS", response.supported_panels)
        self.assertIn("HBA1C", response.supported_panels)
        self.assertIsNotNone(response.timestamp)

if __name__ == "__main__":
    unittest.main()
