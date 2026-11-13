# Product Requirements Document (PRD): ReportSaathi

**Document Reference:** `docs/05-prd.md`  
**Product Version:** MVP (v1.0)  
**Based on:** `docs/01-problem.md`, `docs/02-research.md`, `docs/03-scope.md`, and `docs/04-design.md`  
**Target Market:** India (Urban and semi-urban patients, elderly chronic disease managers, and family caregivers)  
**Regulatory Posture:** Educational Health Literacy Tool (Exempt from CDSCO SaMD; compliant with DPDP Act 2023 and NMC Telemedicine Guidelines 2020)

---

## 1. Product Goals & Non-Goals

### 1.1 Goals
1. **Demystify Routine Blood Reports:** Convert confusing medical biomarkers and biological reference tables (starting with Fasting Blood Sugar, HbA1c, and Lipid Profile) into plain, everyday language in under 10 seconds.
2. **Empower Doctor Consultations:** Equip patients and family caregivers with 2–3 structured, doctor-vetted, non-alarmist questions to carry directly into their outpatient (OPD) clinic visit.
3. **Bridge the Caregiver Communication Gap:** Enable digitally literate family members (the "Nephew" persona) to easily generate and forward a verified, lightweight summary card to elderly parents via WhatsApp.
4. **Reduce Consultation Delays:** Eliminate the dangerous 1–3 week post-test delay caused by incomprehension, fear of bad news, or reliance on informal family WhatsApp advice.
5. **Airtight Legal & Clinical Safety:** Ensure 100% deterministic compliance with Indian health regulations by strictly avoiding clinical diagnosis, triage scoring, and treatment modification.

### 1.2 Non-Goals (Strict Boundaries)
1. **NO Medical Diagnosis:** The product will never tell a user they have a disease (e.g., *"You have Type 2 Diabetes"* or *"This indicates fatty liver disease"*).
2. **NO Treatment or Dosage Advice:** The product will never advise patients on what medications, dosages, or home remedies to start, alter, or discontinue (e.g., *"Take 500mg Metformin"*, *"Stop your statin"*).
3. **NO Universal Color-Coded Triage Bands:** The product will never output bright green/yellow/red "traffic light" bands that declare a patient "Safe" or "In Danger", preventing fatal false reassurance.
4. **NO Prescription Verification:** The product will not evaluate whether a doctor’s prescribed medicine or dosage is clinically appropriate.
5. **NO Commercial Health Upselling:** The product will never sell medicines, push partner teleconsultations, advertise Ayurvedic supplements, or monetize patient health anxieties.
6. **NO Persistent Health Record Locker:** In this MVP, the product will not act as a permanent Electronic Health Record (EHR) database or cloud vault; all processing is ephemeral to preserve strict data privacy under the DPDP Act 2023.
7. **NO Native App Download:** The product will not require an iOS/Android app store download; it operates as an instant, zero-login mobile web tool and WhatsApp companion card.

---

## 2. User Personas & User Stories

### 2.1 Personas
* **Rahul (28, Family Caregiver / "The Nephew"):** Tech-literate, urban professional. His retired parents and extended family in Tier-2 cities WhatsApp him photos of lab reports asking *"Batao kya hai"* (tell us what this is). He wants a quick, factual, safe explanation without alarming his family or bugging his doctor friends late at night.
* **Ramesh Kumar (62, Chronic Health Patient):** Reads basic conversational English but is bewildered by Latin/Greek medical terms on his lab reports (*"Estimated Avg Glucose"*, *"Glycosylated Hemoglobin"*). Suffers from anxiety when seeing bold red numbers. Needs simple words and clear questions for his physician.
* **Dr. Anita Deshmukh (45, Primary Care Physician / General Physician):** Runs a busy OPD clinic seeing 40+ patients a day (avg. 4–6 minutes per patient). Frustrated by patients who arrive with ChatGPT-induced panic about cancer or who delayed treatment by taking unvetted WhatsApp remedies. Welcomes patients who arrive with concise, structured questions.

### 2.2 User Stories

| ID | As a... | I want to... | So that... |
| :--- | :--- | :--- | :--- |
| **US-01** | Caregiver (Rahul) | Take a photo of my uncle's blood test report and upload it without creating an account | I can quickly get an objective breakdown without wading through registration forms. |
| **US-02** | Caregiver (Rahul) | Verify that the extracted numbers and lab ranges match the paper report | I am 100% confident the system did not misread the numbers before I show it to family. |
| **US-03** | Elderly Patient (Ramesh) | Read what each test measures in simple words (English and Hindi) | I understand why my doctor ordered the test and what the biomarker represents in everyday life. |
| **US-04** | Patient / Caregiver | Receive a simple 3-line summary of what is within or outside the lab's printed range | I know the general status without experiencing white-coat panic or seeing terrifying disease lists. |
| **US-05** | Patient / Caregiver | Get 2–3 structured questions prepared for my doctor visit | I can carry actionable questions into the clinic and make the most of my doctor's limited time. |
| **US-06** | Caregiver (Rahul) | Forward the plain summary and questions as a clean card directly over WhatsApp | My uncle and treating physician can review it on their own phones without installing an app. |
| **US-07** | Treating Doctor (Dr. Anita) | Have my patient arrive with clear questions instead of misinformed AI cyberchondria | I can spend the consultation addressing their actual health management rather than undoing panic. |

---

## 3. Numbered Functional Requirements (FR)

### Module 1: Ingestion & Verification
* **FR-1.1: Multi-Format Ingestion:** The system shall accept blood test report uploads in JPG, PNG, and single-page PDF formats up to 10MB.
* **FR-1.2: Client-Side Pre-Compression:** The system shall compress captured images in the browser before upload (targeting $< 250\text{ KB}$) to ensure reliability on 2G/3G connections.
* **FR-1.3: Scope Capping (Pilot Panels):** The system shall strictly target and process routine metabolic and lipid parameters:
  * Fasting Blood Sugar (FBS)
  * Post-Prandial Blood Sugar (PPBS)
  * HbA1c (Glycated Hemoglobin)
  * Total Cholesterol
  * Triglycerides
  * HDL Cholesterol
  * LDL Cholesterol
* **FR-1.4: Extraction of Lab Stated Reference Ranges:** The system shall extract both the patient's observed value and the **specific reference interval printed on that lab's report** rather than substituting hardcoded global defaults.
* **FR-1.5: Human-in-the-Loop Verification Screen:** Before generating the final card, the system shall present an interactive verification screen displaying extracted parameters side-by-side with original cropped report snippets, allowing the user to confirm or edit numbers.

### Module 2: Translation & Non-Diagnostic Analysis
* **FR-2.1: Deterministic Jargon Swapper:** The system shall map extracted biomarkers to plain-language descriptions using a deterministic, doctor-vetted dictionary (e.g., *"HbA1c"* $\rightarrow$ *"Your average blood sugar level over the past 3 months"*).
* **FR-2.2: Bilingual Explanations:** The system shall provide explanations in conversational English and Hindi (Devanagari script) side-by-side.
* **FR-2.3: Factual Range Status Tagging:** The system shall compare the extracted numerical value against the lab's printed range and assign one of three factual tags:
  * `WITHIN_LAB_RANGE`
  * `OUTSIDE_LAB_RANGE`
  * `INDETERMINATE_RANGE` (if range was smudged or unreadable)
* **FR-2.4: Prohibition of Triage Scoring:** The system shall **not** assign severity scores (e.g., *"Mild"*, *"Critical"*), and shall **not** apply color-coded triage bands (Green/Yellow/Red). Out-of-range values shall be displayed in a neutral Ochre tag.

### Module 3: Summary & Question Generation
* **FR-3.1: Three-Line Plain Summary:** The system shall generate a structured 3-line textual recap:
  * *Line 1:* Biomarkers tested on this report.
  * *Line 2:* Which biomarkers are outside the lab's stated printed reference interval.
  * *Line 3:* An objective, doctor-affirming reminder to review these findings with the treating physician.
* **FR-3.2: "Questions for Your Doctor" Engine:** The system shall select 2–3 curated, clinically validated questions mapped to the detected out-of-range parameters (e.g., *"My 3-month sugar is 6.8%. Do you recommend lifestyle modifications first, or medication?"*).
* **FR-3.3: In-Clinic Checklist Affordance:** The question list shall include tick-boxes so patients can visually check off items during their consultation.

### Module 4: Delivery, Sharing & Lifecycle
* **FR-4.1: WhatsApp Forward Card Generator:** The system shall generate a lightweight, high-contrast visual card (PNG) and pre-formatted WhatsApp text payload for instant forwarding via `https://wa.me/` or native Android share intent.
* **FR-4.2: Statutory Disclaimer:** Every generated screen, visual card, and text export shall include an un-editable statutory disclaimer:  
  *"ReportSaathi is an educational health literacy tool, not a diagnostic medical device. It does not provide medical advice or diagnosis. Always consult a Registered Medical Practitioner (RMP)."*
* **FR-4.3: Ephemeral Data Purge:** The system shall process uploaded images entirely in memory. Uploaded files and extracted patient metrics shall be permanently purged immediately after card generation (zero persistent server-side database storage).

---

## 4. Non-Functional Requirements (NFR)

### 4.1 Performance & Latency
* **NFR-1.1 Processing Speed:** Total end-to-end turnaround time from photo upload to card rendering shall not exceed **8.0 seconds** on a standard 3G/4G cellular connection.
* **NFR-1.2 Lightweight Bundle Size:** Total frontend assets (HTML, CSS, JS) shall not exceed **200 KB** gzipped, ensuring sub-second rendering on budget Android devices.
* **NFR-1.3 Low-RAM Optimization:** The frontend shall maintain a DOM footprint under 120 nodes with zero memory leaks, preventing Chrome crashes on 1GB/2GB RAM Android Go devices.

### 4.2 Usability & Accessibility
* **NFR-2.1 Contrast Standards:** All body text and background pairings shall strictly comply with **WCAG 2.1 AAA** (contrast ratio $\ge 7.0:1$ for body text, $\ge 4.5:1$ for large headings).
* **NFR-2.2 Touch Targets:** All primary buttons and interactive elements shall have a minimum physical touch target of **56dp** in height to accommodate elderly users and unsteady hands.
* **NFR-2.3 Typography & Script Rendering:** 
  * Minimum body font size: **16sp**.
  * Line-height: **1.55x to 1.6x** to ensure Devanagari vowel signs (*matras*) and conjuncts never clip vertically.
  * Word wrapping: All text containers must enforce `overflow-wrap: break-word` and `hyphens: auto` to prevent horizontal overflow of long Indic compound words.

### 4.3 Privacy & Legal Compliance (DPDP Act 2023)
* **NFR-3.1 Ephemeral Execution:** Zero persistent storage of personal data or diagnostic reports. No database containing health records shall exist.
* **NFR-3.2 Encryption in Transit:** All client-server communications shall enforce **TLS 1.3** with strict HTTPS transport security.
* **NFR-3.3 Zero Tracker Footprint:** Zero third-party advertising SDKs, tracking pixels, or commercial analytics trackers shall be integrated into the product.

---

## 5. Safety & Regulatory Requirements

* **SR-1: CDSCO SaMD Exemption Rule:** The software must strictly operate as an informational and formatting aid. It shall not perform patient-specific risk calculation, automated triage, or treatment selection.
* **SR-2: NMC Telemedicine Guidelines Rule:** The tool shall not issue prescriptions, alter dosages, or endorse specific pharmaceutical or commercial remedies.
* **SR-3: Hallucination & Anxiety Circuit-Breaker:** The system shall use **deterministic lookup tables** for biomarker definitions and doctor questions. Generative LLMs shall **never** be permitted to generate unconstrained medical advice, speculative disease lists, or differential diagnoses.
* **SR-4: Tone Guardrails:** Copywriting must remain strictly neutral, calm, and doctor-affirming. Words such as *"Dangerous"*, *"Fatal"*, *"Cancer"*, *"Emergency"*, and *"Alarming"* are strictly blacklisted from the dictionary.

---

## 6. Success Metrics & Key Performance Indicators (KPIs)

```
                       [ SUCCESS METRIC PYRAMID ]
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
[ CONSULTATION IMPACT ]                             [ SAFETY & ACCURACY ]
- Doctor Question Carry-In Rate (>= 40%)             - Zero Misleading Reassurances (0%)
- Time-to-Consultation Delay (<= 4 days)            - OCR Extraction Accuracy (>= 98%)
- Patient Comprehension Score (>= 4.5 / 5)           - Zero CDSCO / DPDP Infractions
```

| Metric Category | Specific Indicator | Target (4-Week Pilot) | Measurement Methodology |
| :--- | :--- | :--- | :--- |
| **Primary Value Delivery** | **Doctor Question Carry-In Rate** | $\ge \mathbf{40\%}$ | In-clinic exit survey asking patients if they carried and referenced the question card during the OPD visit. |
| **Delay Reduction** | **Time-to-Consultation** | $\le \mathbf{4\text{ days}}$ | Average days between report release and doctor visit (reduced from traditional baseline of 14+ days). |
| **Comprehension** | **Self-Reported Clarity Score** | $\ge \mathbf{4.5 / 5.0}$ | Single-question prompt on share screen: *"Did this summary help you understand your test?"* |
| **Clinical Safety** | **Diagnostic Intrusion Rate** | $\mathbf{0.0\%}$ | Zero instances of the system generating a disease label or treatment alteration. |
| **Extraction Accuracy** | **Parameter Extraction Precision** | $\ge \mathbf{98.0\%}$ | Percentage of OCR extractions confirmed without manual digit correction on the review screen. |
| **Caregiver Virality** | **WhatsApp Share Rate** | $\ge \mathbf{55\%}$ | Percentage of generated summaries shared via WhatsApp or copied to clipboard. |
