# Clinical & Regulatory Safety Rules: ReportSaathi

**Document Reference:** `docs/06b-safety-rules.md`  
**Applicability:** Core Engine, Deterministic Rule Handlers, LLM Fallback Pipelines, and Frontend UI Copy  
**Statutory Foundation:** CDSCO Medical Device Rules (MDR) 2017 / SaMD Guidelines, Telemedicine Practice Guidelines 2020 (NMC Act 2019), Digital Personal Data Protection Act 2023 (DPDP Act), and Consumer Protection Act 2019  
**Core Safety Motto:** *"Educate and Empower, Never Diagnose or Prescribe."*

---

## 1. Statutory Context & Regulatory Boundaries

In India, software providing health-related information crosses into **unauthorized medical practice** and **Class B Medical Device regulation (SaMD)** the moment it performs autonomous clinical decision-making, disease diagnosis, or treatment intervention. 

To maintain strict regulatory exemption as an **educational health literacy tool**, ReportSaathi enforces **Eight Inviolable Safety Rules**. Any code, feature, prompt, or UI copy that violates these rules is rejected.

---

## 2. The Eight Inviolable Safety Rules

```
                      [ REPORT SAATHI SAFETY FRAMEWORK ]
                                       │
     ┌─────────────────────────────────┼─────────────────────────────────┐
     ▼                                 ▼                                 ▼
[ 1. ZERO DIAGNOSIS ]        [ 2. ZERO TREATMENT ]            [ 3. NO TRAFFIC LIGHTS ]
No disease labels            No drug / dosage changes         No green/yellow/red bands
No differential lists        No home remedies                 No false reassurance
     │                                 │                                 │
     ├─────────────────────────────────┼─────────────────────────────────┤
     ▼                                 ▼                                 ▼
[ 4. BIND LAB RANGES ]       [ 5. AFFIRM DOCTOR ]             [ 6. EPHEMERAL DATA ]
Never hardcode ranges        Every card prompts RMP           Zero disk retention
Respect lab machine          Human in the loop                Zero model training
     │                                 │                                 │
     └─────────────────────────────────┴─────────────────────────────────┘
```

---

### Rule 1: The Diagnostic Prohibition (Zero Disease Labeling)
* **The Rule:** The system shall **never** assign, speculate, or output a medical diagnosis, disease label, syndromic classification, or differential diagnosis.
* **Prohibited Outputs:**
  * ❌ *"You have Type 2 Diabetes."*
  * ❌ *"This indicates pre-diabetes."*
  * ❌ *"High cholesterol suggests early cardiovascular disease or atherosclerosis."*
  * ❌ *"Possible differential diagnoses include Cushing's syndrome or pancreatitis."*
* **Permitted Output (Factual Translation Only):**
  * ✅ *"Fasting Blood Sugar measures sugar in your bloodstream after an overnight fast. Your result is 114 mg/dL. The reference range printed by your lab is 70 to 99 mg/dL."*
* **Enforcement Mechanism:**
  * Deterministic regex scrubber scans all generated copy. If any word from the **Diagnostic Blacklist** (see Section 3) is detected, the request is immediately intercepted and replaced with the fallback deterministic template.

---

### Rule 2: The Treatment & Pharmacological Prohibition (Zero Medical Advice)
* **The Rule:** The system shall **never** recommend starting, stopping, increasing, or decreasing any medication, pharmaceutical product, dietary supplement, or clinical intervention.
* **Prohibited Outputs:**
  * ❌ *"Start taking 500mg Metformin once daily."*
  * ❌ *"You should reduce your statin dose."*
  * ❌ *"Drink bitter gourd (karela) juice to bring down your blood sugar."*
  * ❌ *"Avoid all carbohydrates until your next blood test."*
* **Permitted Output (Question for Physician):**
  * ✅ *"Ask your doctor: 'My 3-month sugar average is 6.8%. Do you recommend modifying my diet and physical activity first, or starting medication?'"*
* **Enforcement Mechanism:**
  * Prescriptive action verbs (*"take"*, *"stop"*, *"administer"*, *"ingest"*, *"dose"*) are strictly barred from the recommendation generator. Questions can only take the form of inquiry directed to the Registered Medical Practitioner (RMP).

---

### Rule 3: The Anti-Alarmist Visual Rule (Prohibition of Traffic Light Colors)
* **The Rule:** The system shall **never** display universal Green, Yellow, or Red color bands on lab parameters.
* **Clinical Rationale:**
  * **The Green Band Hazard:** A universal "Green = Safe" label creates dangerous **false reassurance**. For example, a fasting blood sugar of 105 mg/dL is pre-diabetic for a normal adult, but constitutes dangerous gestational diabetes in a pregnant woman. A "Green" label could cause a pregnant mother to skip essential follow-ups, creating life-threatening clinical harm and extreme liability under the Consumer Protection Act, 2019.
  * **The Red Band Hazard:** Flashing red banners cause acute panic, white-coat hypertension spikes, and impulsive self-medication.
* **Color Standard:**
  * Parameter within printed range: Neutral Slate Card (`#F8FAFC`).
  * Parameter outside printed range: Neutral Calm Ochre Tag (`#FEF3C7` / `#92400E`) labeled strictly: *"Outside Lab Printed Range"*.

---

### Rule 4: Machine-Specific Interval Respect (Anti-Hardcoding Rule)
* **The Rule:** The system shall **never** evaluate numbers against hardcoded textbook reference ranges. It must strictly compare values against the **specific reference interval printed on that individual lab's report**.
* **Clinical Rationale:**
  * Reference intervals vary significantly across diagnostic methods (e.g., Hexokinase vs Glucose Oxidase; HPLC vs Immunoassay). Evaluating a patient’s value against an arbitrary textbook range misclassifies normal patients as abnormal or vice-versa.
* **Handling Missing / Obscured Ranges:**
  * If the lab's printed range is torn, smudged, or unreadable, the system shall mark the parameter status as `INDETERMINATE_RANGE` and prompt the user to inspect the paper document. It shall **never guess or substitute a standard range**.

---

### Rule 5: Doctor-Affirming Mediation & Non-Intermediary Principle
* **The Rule:** The product shall always position the human physician as the sole clinical authority. The output must act as a bridge into the clinic, never as a substitute for an OPD visit.
* **Formatting Directives:**
  * Every card must feature the section: *"Questions for Your Doctor / डॉक्टर से पूछने के सवाल"*.
  * Questions must be phrased respectfully to facilitate constructive physician-patient dialogue without offending the doctor.
  * The statutory non-diagnostic disclaimer must be permanently visible on all shared images and text payloads.

---

### Rule 6: Ephemeral Data Lifecycle & Zero Storage (DPDP Compliance)
* **The Rule:** Personal Health Data (PHD) shall never be persisted to disk, stored in databases, or used for model training.
* **Lifecycle Directives (DPDP Act 2023, Section 8):**
  1. Uploaded image buffer exists exclusively in volatile memory (RAM).
  2. OCR extraction executes in ephemeral sandbox memory.
  3. Image buffer and extracted values are permanently garbage-collected immediately upon HTTP response transmission.
  4. Server logs shall never log raw text, patient names, or biological values; logs only record timestamp, status code, and latency.

---

### Rule 7: Human-in-the-Loop Verification Requirement
* **The Rule:** The system shall **never** generate a plain-language summary directly from automated OCR without explicit user confirmation.
* **Operational Flow:**
  * An intermediate screen (`Screen-03-Review`) presents the extracted numbers alongside cropped source snippets.
  * The user must tap *"Numbers Match My Report"* (or edit any smudged digit) before the summary card is rendered.
  * This guarantees that any OCR misread (e.g., reading `174` as `114`) is caught by human eyes, eliminating automated extraction liability.

---

### Rule 8: Strict LLM Jailbreak & Circuit-Breaker Guardrails
* **The Rule:** If an AI model / LLM is invoked as a fallback for OCR parsing or natural phrasing, it must operate within a rigid, deterministic harness.
* **System Prompt Harness:**
  ```text
  You are an educational health literacy assistant.
  Your ONLY task is to rephrase extracted lab values into plain everyday language.
  
  CRITICAL SAFETY MANDATES:
  1. NEVER diagnose a disease or condition (do not use words like diabetes, hypertension, illness).
  2. NEVER suggest medication, remedies, or dosage changes.
  3. NEVER state that a level is dangerous, fatal, or safe.
  4. ONLY explain what the biological parameter measures in everyday terms.
  5. ONLY suggest 2 questions for the patient to ask their doctor.
  6. If asked for medical advice, reply: "Please consult your Registered Medical Practitioner."
  ```
* **Post-Generation Circuit-Breaker:**
  * Before returning any LLM output to the client, the backend executes an automated regex filter against the **Forbidden Term Blacklist**.
  * If a violation is detected, the entire LLM response is discarded, and the system reverts to the static hardcoded template dictionary.

---

## 3. Blacklist of Forbidden Terms & Diagnostic Scrubber

The following terms are hard-coded into the backend regex validation interceptor:

```python
FORBIDDEN_DIAGNOSTIC_TERMS = [
    # Diseases & Diagnostic Labels
    r"\bdiabet(es|ic)\b",
    r"\bpre-?diabet(es|ic)\b",
    r"\bhypertens(ion|ive)\b",
    r"\batherosclero(sis|tic)\b",
    r"\bhyperlipid(emia|emic)\b",
    r"\bmetabolic syndrome\b",
    r"\bchronic kidney disease\b",
    r"\brenal failure\b",
    r"\bneoplasm\b",
    r"\bcancer\b",
    r"\btumor\b",
    r"\bnephropathy\b",
    r"\bretinopathy\b",
    r"\bneuropathy\b",
    r"\bischemi(a|c)\b",
    r"\binfarction\b",
    
    # Prescriptive & Treatment Verbs
    r"\btake \d+\s*(mg|ml|tablets?|capsules?)\b",
    r"\bstart taking\b",
    r"\bstop taking\b",
    r"\bdiscontinue\b",
    r"\bincrease dose\b",
    r"\bdecrease dose\b",
    r"\bprescribe\b",
    r"\bmetformin\b",
    r"\bstatin(s)?\b",
    r"\binsulin\b",
    r"\batorvastatin\b",
    
    # Alarmist & Emotional Adjectives
    r"\bdangerous(ly)?\b",
    r"\bfatal\b",
    r"\bdeadly\b",
    r"\balarming(ly)?\b",
    r"\bpanic\b",
    r"\bemergency\b",
    r"\bcatastrophic\b",
    r"\bhospitalize\b"
]
```

---

## 4. Mandatory Statutory Disclaimer

Every screen, shared PNG image, and WhatsApp text snippet must display the exact statutory notice below:

```text
⚖️ STATUTORY NOTICE (REPORT SAATHI):
ReportSaathi is an educational health literacy tool, not a medical device.
It does not diagnose conditions, interpret individual clinical risk, or recommend treatments.
All lab results must be clinically correlated by a Registered Medical Practitioner (RMP).
```
