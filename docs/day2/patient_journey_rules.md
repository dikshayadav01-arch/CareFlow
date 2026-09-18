# CareFlow — Patient Journey Rules

## 1. Objective

The CareFlow simulator will generate synthetic hospital patient journeys.

Each patient's journey will consist of multiple timestamped activities.

The generator will introduce normal process variation and selected
process inefficiencies so that process mining can later identify them.

---

## 2. Pathway Types

### Normal Pathway

Registration
→ Triage
→ Doctor Consultation
→ Investigation
→ Treatment
→ Discharge

### X-Ray Pathway

Registration
→ Triage
→ Doctor Consultation
→ X-Ray
→ Treatment
→ Discharge

### X-Ray Loop-Back Pathway

Registration
→ Triage
→ Doctor Consultation
→ X-Ray
→ Triage
→ Doctor Consultation
→ Treatment
→ Discharge

---

## 3. Patient Attributes

The simulator will generate:

- Case_ID
- Patient_ID
- Age_Group
- Gender
- Emergency_Level
- Doctor
- Department

---

## 4. Process Variation

Different patients may have different:

- Waiting times
- Doctors
- Emergency levels
- Investigation requirements
- X-Ray requirements
- Process durations

---

## 5. Process Inefficiency

The simulator will introduce selected inefficient pathways.

One important inefficiency is the X-Ray loop-back:

X-Ray
→ Triage
→ Doctor Consultation

This represents a patient being sent back through part of the
process after the investigation.

The reason for the loop-back is simulated as a process issue,
such as incomplete documentation or missing information.

---

## 6. Process Mining Goals

The generated data should allow CareFlow to discover:

1. Common patient pathways
2. Rare process variants
3. Repeated activities
4. X-Ray loop-backs
5. Long transitions
6. Bottleneck activities
7. Process deviations
8. Differences between actual and ideal pathways

---

## 7. Data Generation Principle

The generator will create the event log first.

Analysis will be performed separately.

The simulator must not directly calculate or claim the final
business findings.

For example, the generator may create loop-back cases,
but the final loop-back percentage will be calculated later
from the generated event log.