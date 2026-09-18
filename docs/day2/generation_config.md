# CareFlow — Synthetic Data Generation Configuration

## 1. Dataset Size

Initial development dataset:

- Patients: 100
- Events: variable depending on patient pathway

The dataset size will be increased later for the final project.

---

## 2. Patient Demographics

### Age Groups

- 0-17
- 18-24
- 25-34
- 35-44
- 45-54
- 55-64
- 65+

### Gender

- Male
- Female
- Other

---

## 3. Emergency Levels

The simulator will use:

- Low
- Medium
- High
- Critical

Emergency level may influence waiting and processing times.

---

## 4. Doctors

Synthetic doctors:

- Dr. Sharma
- Dr. Verma
- Dr. Singh
- Dr. Gupta
- Dr. Mehta

---

## 5. Departments

The simulator may use:

- Emergency
- Radiology
- Laboratory
- Pharmacy

---

## 6. Pathway Selection

Each patient will be assigned a pathway.

Possible pathways:

1. Normal pathway
2. X-Ray pathway
3. X-Ray loop-back pathway

The pathway will be selected probabilistically.

The exact final proportions will be measured from the generated data.

---

## 7. Timestamp Generation

Each activity will have a timestamp.

The timestamp of a later activity must always be greater than
the timestamp of the previous activity.

The simulator will generate variable waiting and processing
durations instead of using the exact same duration for every patient.

---

## 8. Repeated Activities

Loop-back patients will contain repeated activities.

Example:

X-Ray
→ Triage
→ Doctor Consultation

These repeated activities are intentional process variations
that will later be detected using process mining.

---

## 9. Synthetic Data Requirement

All generated information must be fictional.

No real patient names, medical record numbers,
addresses, phone numbers, or other real personally
identifiable information will be generated.

---

## 10. Reproducibility

The Python generator should use a fixed random seed during
development.

This allows the same dataset to be reproduced when testing
the pipeline.