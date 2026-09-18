# CareFlow — EHR Event Log Schema

## 1. Purpose

CareFlow uses a synthetic Electronic Health Record (EHR) event log
to represent patient journeys through a hospital.

Each row represents one event/activity performed during a patient's journey.

The data is completely synthetic and does not contain real patient information.

---

## 2. Event Log Fields

| Field | Description | Example |
|---|---|---|
| Case_ID | Unique identifier for one complete patient journey | C0001 |
| Patient_ID | Synthetic patient identifier | P0001 |
| Activity_Name | Hospital activity performed | Triage |
| Timestamp | Date and time of the activity | 2026-01-10 09:15:00 |
| Department | Hospital department | Emergency |
| Doctor | Doctor responsible for the activity | Dr. Sharma |
| Emergency_Level | Patient urgency level | Medium |
| Age_Group | Patient age category | 25-34 |
| Gender | Synthetic patient gender | Female |

---

## 3. Primary Patient Pathway

A normal emergency-care journey can follow:

Registration
→ Triage
→ Doctor Consultation
→ Investigation
→ Treatment
→ Discharge

---

## 4. X-Ray Patient Pathway

Some patients require an X-Ray:

Registration
→ Triage
→ Doctor Consultation
→ X-Ray
→ Treatment
→ Discharge

---

## 5. Loop-Back Pathway

Some X-Ray cases may experience a process loop:

Registration
→ Triage
→ Doctor Consultation
→ X-Ray
→ Triage
→ Doctor Consultation
→ Treatment
→ Discharge

The repeated Triage and Doctor Consultation activities represent
a process loop-back.

The generator will create these cases synthetically.
The actual loop-back percentage will later be calculated from the generated event log.

---

## 6. Process Mining Objective

The event log will later be analyzed using PM4Py to discover:

- Most common patient pathways
- Process variants
- Repeated activities
- Loop-backs
- Bottlenecks
- Transition times
- Deviations from the expected pathway
- Conformance with an ideal process

---

## 7. Privacy

All patient information in CareFlow is synthetic.

No real patient records, medical records, personally identifiable information,
or hospital databases are used.