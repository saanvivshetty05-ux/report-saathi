/**
 * ReportSaathi Shared Types & API Contract
 * Source of truth: docs/06a-api-contract.md and shared/schemas/contract.json
 */

export type RangeStatus = "WITHIN_LAB_RANGE" | "OUTSIDE_LAB_RANGE" | "INDETERMINATE";

export interface HealthResponse {
  status: "healthy" | "degraded" | "unhealthy";
  version: string;
  database_status: "connected" | "disconnected" | "error";
  database_value: string;
  ocr_engine_available: boolean;
  supported_panels: string[];
  timestamp: string;
}

export interface BiomarkerExtraction {
  parameter_code: string;
  display_name_en: string;
  display_name_hi: string;
  observed_value: number;
  unit: string;
  lab_range_low?: number | null;
  lab_range_high?: number | null;
  status: RangeStatus;
  ocr_confidence: number;
}

export interface ConfirmedParameter {
  parameter_code: string;
  observed_value: number;
  unit: string;
  lab_range_low?: number | null;
  lab_range_high?: number | null;
}

export interface VerificationPayload {
  session_id: string;
  language?: string;
  confirmed_parameters: ConfirmedParameter[];
}

export interface DoctorQuestion {
  id: string;
  question_en: string;
  question_hi: string;
}

export interface DecodedBiomarker {
  parameter_code: string;
  name_en: string;
  name_hi: string;
  observed_value: number;
  unit: string;
  lab_range: string;
  status_tag: string;
  plain_explanation_en: string;
  plain_explanation_hi: string;
}

export interface ReportSummaryLines {
  line_1: string;
  line_2: string;
  line_3: string;
}

export interface WhatsAppPayload {
  encoded_url: string;
  plain_text: string;
}

export interface FinalReportCard {
  session_id: string;
  summary: ReportSummaryLines;
  decoded_biomarkers: DecodedBiomarker[];
  doctor_questions: DoctorQuestion[];
  statutory_disclaimer: string;
  whatsapp_payload: WhatsAppPayload;
}

export interface StandardErrorPayload {
  success: false;
  error: {
    code: string;
    message: string;
    suggested_action?: string;
    timestamp: string;
  };
}
