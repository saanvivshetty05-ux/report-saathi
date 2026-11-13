# API Contract Specification: ReportSaathi

**Document Reference:** `docs/06a-api-contract.md`  
**API Version:** `v1.0.0`  
**Base Protocol:** HTTPS / REST over TLS 1.3  
**Data Format:** JSON (`application/json`) and Multipart Form (`multipart/form-data`)  
**Statutory Privacy Standard:** DPDP Act 2023 Section 8 (Stateless processing, zero persistent PII storage)

---

## 1. Global Conventions & Standard Error Format

### 1.1 HTTP Status Codes
* `200 OK`: Request succeeded, response body contains JSON payload.
* `400 Bad Request`: Validation failure (unsupported file type, malformed payload, missing parameters).
* `413 Payload Too Large`: Upload exceeds maximum limit of 10 MB.
* `415 Unsupported Media Type`: File format is not JPG, PNG, or PDF.
* `422 Unprocessable Entity`: OCR engine failed to extract readable text, or document is not a supported blood report.
* `429 Too Many Requests`: Rate limit exceeded (default: 10 extractions / IP / hour).
* `500 Internal Server Error`: Server failure; memory buffer safely purged.

### 1.2 Standardized Error Envelope
All error responses return a standardized JSON structure:

```json
{
  "success": false,
  "error": {
    "code": "BLURRY_IMAGE_ERROR",
    "message": "The uploaded photo is too blurry or dark to accurately detect numbers.",
    "suggested_action": "Please retake the photo under bright room light and avoid reflections.",
    "timestamp": "2026-11-13T08:30:00Z"
  }
}
```

---

## 2. API Endpoints

### 2.1 Health Check & Readiness Probe
* **Endpoint:** `GET /api/health`
* **Description:** Health check probe for container readiness, service uptime, and operational database connectivity.
* **Request:** No parameters or headers required.
* **Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database_status": "connected",
  "database_value": "ReportSaathi System v1.0 Operational",
  "ocr_engine_available": true,
  "supported_panels": ["FBS", "PPBS", "HBA1C", "LIPID_PROFILE"],
  "timestamp": "2026-11-13T08:30:00Z"
}
```

---

### 2.2 Ingest & Extract Report Parameters
* **Endpoint:** `POST /api/v1/extract`
* **Description:** Ingests a report image or PDF, preprocesses with OpenCV, runs Tesseract OCR, applies regex extraction for Sugar & Lipid panels, and returns raw extracted parameters for human-in-the-loop verification.
* **Request Format:** `multipart/form-data`
* **Request Fields:**
  * `file` (binary, required): Image file (JPG/PNG) or single-page PDF ($\le 10\text{ MB}$).
  * `language` (string, optional): `"en"` (default) or `"hi"`.
* **Response (200 OK):**
```json
{
  "success": true,
  "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "document_type": "BLOOD_TEST_REPORT",
  "extracted_parameters": [
    {
      "parameter_code": "FBS",
      "display_name_en": "Fasting Blood Sugar",
      "display_name_hi": "फास्टिंग ब्लड शुगर",
      "observed_value": 114.0,
      "unit": "mg/dL",
      "lab_range_low": 70.0,
      "lab_range_high": 99.0,
      "status": "OUTSIDE_LAB_RANGE",
      "ocr_confidence": 0.94
    },
    {
      "parameter_code": "HBA1C",
      "display_name_en": "HbA1c (Glycosylated Hemoglobin)",
      "display_name_hi": "एचबीए1सी (3-महीने का औसत शुगर)",
      "observed_value": 6.8,
      "unit": "%",
      "lab_range_low": 4.0,
      "lab_range_high": 5.6,
      "status": "OUTSIDE_LAB_RANGE",
      "ocr_confidence": 0.96
    }
  ],
  "unsupported_parameters_detected": [],
  "verification_required": true
}
```
* **Error Responses:**
  * `413 Payload Too Large`: `{"error": {"code": "FILE_TOO_LARGE", "message": "File exceeds 10MB limit."}}`
  * `415 Unsupported Media Type`: `{"error": {"code": "INVALID_MIME_TYPE", "message": "Only JPG, PNG, and PDF allowed."}}`
  * `422 Unprocessable Entity`: `{"error": {"code": "NO_BLOOD_TEST_FOUND", "message": "No glucose or lipid test parameters detected in this image."}}`

---

### 2.3 Generate Plain Summary & Doctor Questions
* **Endpoint:** `POST /api/v1/generate-card`
* **Description:** Ingests user-verified parameters, runs deterministic medical jargon swapping and question matching, and returns the final report payload.
* **Request Format:** `application/json`
* **Request Body:**
```json
{
  "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "language": "en",
  "confirmed_parameters": [
    {
      "parameter_code": "FBS",
      "observed_value": 114.0,
      "unit": "mg/dL",
      "lab_range_low": 70.0,
      "lab_range_high": 99.0
    },
    {
      "parameter_code": "HBA1C",
      "observed_value": 6.8,
      "unit": "%",
      "lab_range_low": 4.0,
      "lab_range_high": 5.6
    }
  ]
}
```
* **Response (200 OK):**
```json
{
  "success": true,
  "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "summary": {
    "line_1": "You tested Fasting Blood Sugar and HbA1c (3-month sugar average).",
    "line_2": "Fasting Sugar (114 mg/dL) and HbA1c (6.8%) fall outside your lab's printed range.",
    "line_3": "No emergency action is needed today. Please show these results to your treating doctor this week."
  },
  "decoded_biomarkers": [
    {
      "parameter_code": "HBA1C",
      "name_en": "HbA1c (Glycosylated Hemoglobin)",
      "name_hi": "एचबीए1सी",
      "observed_value": 6.8,
      "unit": "%",
      "lab_range": "4.0 - 5.6 %",
      "status_tag": "Outside Lab Printed Range",
      "plain_explanation_en": "This test measures your average blood sugar over the last 3 months. It reflects your long-term trend, not what you ate yesterday.",
      "plain_explanation_hi": "यह परीक्षण पिछले 3 महीनों में आपके रक्त में औसत शुगर का स्तर बताता है।"
    },
    {
      "parameter_code": "FBS",
      "name_en": "Fasting Blood Sugar",
      "name_hi": "फास्टिंग ब्लड शुगर",
      "observed_value": 114.0,
      "unit": "mg/dL",
      "lab_range": "70 - 99 mg/dL",
      "status_tag": "Outside Lab Printed Range",
      "plain_explanation_en": "Measures sugar in your bloodstream after an overnight fast (8-10 hours without eating).",
      "plain_explanation_hi": "रात भर भूखे रहने (8-10 घंटे) के बाद सुबह का ब्लड शुगर स्तर।"
    }
  ],
  "doctor_questions": [
    {
      "id": "Q-HBA1C-01",
      "question_en": "My 3-month sugar average is 6.8%. Do you advise lifestyle and dietary adjustments first, or do you recommend starting medication?",
      "question_hi": "मेरा 3 महीने का औसत शुगर 6.8% है। क्या आप पहले खान-पान और जीवनशैली में बदलाव की सलाह देते हैं, या दवा शुरू करने की?"
    },
    {
      "id": "Q-HBA1C-02",
      "question_en": "Are there specific walking or diet targets you want me to maintain before we repeat this test in 3 months?",
      "question_hi": "अगले 3 महीने में दोबारा जांच कराने से पहले क्या मुझे किसी विशेष आहार या चलने के लक्ष्य का पालन करना चाहिए?"
    }
  ],
  "statutory_disclaimer": "ReportSaathi is an educational health literacy tool, not a medical diagnosis device. It does not provide medical advice or diagnosis. Always consult a Registered Medical Practitioner (RMP).",
  "whatsapp_payload": {
    "encoded_url": "https://wa.me/?text=ReportSaathi%20Summary%3A%20...",
    "plain_text": "📋 *ReportSaathi Summary*\n• HbA1c: 6.8% (Lab Range: 4.0-5.6%)\n• Fasting Sugar: 114 mg/dL (Lab Range: 70-99 mg/dL)\n\n❓ *Questions to ask Doctor:*\n1. My 3-month sugar average is 6.8%. Do you advise lifestyle changes first or medication?\n2. Should we repeat this test in 3 months?\n\n_Educational aid only. Always consult your RMP._"
  }
}
```

---

### 2.4 Render Visual Share Card (PNG Image)
* **Endpoint:** `POST /api/v1/render-card-image`
* **Description:** Server-side renders a high-contrast, clean 16:9 PNG image of the report card for WhatsApp status or direct forwarding.
* **Request Format:** `application/json` (Passes the `FinalReportCard` payload from `generate-card`).
* **Response (200 OK):**
  * `Content-Type: image/png`
  * Binary stream of the rendered PNG image.
