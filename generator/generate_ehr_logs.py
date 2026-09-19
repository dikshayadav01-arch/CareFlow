"""
CareFlow - Synthetic EHR Event Log Generator

This module will generate completely synthetic hospital
patient journeys for process mining analysis.
"""

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

# Configuration

RANDOM_SEED = 42
NUM_PATIENTS = 100

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

fake = Faker()
fake.seed_instance(RANDOM_SEED)

# Synthetic reference data

AGE_GROUPS = [
    "0-17",
    "18-24",
    "25-34",
    "35-44",
    "45-54",
    "55-64",
    "65+",
]

GENDERS = [
    "Male",
    "Female",
    "Other",
]

EMERGENCY_LEVELS = [
    "Low",
    "Medium",
    "High",
    "Critical",
]

DOCTORS = [
    "Dr. Sharma",
    "Dr. Verma",
    "Dr. Singh",
    "Dr. Gupta",
    "Dr. Mehta",
]

DEPARTMENTS = [
    "Emergency",
    "Radiology",
    "Laboratory",
    "Pharmacy",
]

# Activity-to-department mapping

ACTIVITY_DEPARTMENTS = {
    "Registration": "Emergency",
    "Triage": "Emergency",
    "Doctor Consultation": "Emergency",
    "Investigation": "Laboratory",
    "X-Ray": "Radiology",
    "Treatment": "Emergency",
    "Discharge": "Emergency",
}

# Pathway selection

PATHWAY_PROBABILITIES = {
    "NORMAL": 0.50,
    "XRAY": 0.30,
    "XRAY_LOOPBACK": 0.20,
}


def select_pathway():
    """
    Randomly select a synthetic patient pathway
    using the configured pathway probabilities.
    """

    pathways = list(PATHWAY_PROBABILITIES.keys())
    probabilities = list(PATHWAY_PROBABILITIES.values())

    return random.choices(
        pathways,
        weights=probabilities,
        k=1,
    )[0]

# Patient activity pathways

PATHWAYS = {
    "NORMAL": [
        "Registration",
        "Triage",
        "Doctor Consultation",
        "Investigation",
        "Treatment",
        "Discharge",
    ],
    "XRAY": [
        "Registration",
        "Triage",
        "Doctor Consultation",
        "X-Ray",
        "Treatment",
        "Discharge",
    ],
    "XRAY_LOOPBACK": [
        "Registration",
        "Triage",
        "Doctor Consultation",
        "X-Ray",
        "Triage",
        "Doctor Consultation",
        "Treatment",
        "Discharge",
    ],
}


def get_pathway_activities(pathway):
    """
    Return the activity sequence for a selected pathway.
    """

    if pathway not in PATHWAYS:
        raise ValueError(f"Unknown pathway: {pathway}")

    return PATHWAYS[pathway]

# Synthetic patient attributes

def generate_patient_attributes(patient_number):
    """
    Generate synthetic demographic and clinical attributes
    for one patient.
    """

    return {
        "Patient_ID": f"P{patient_number:04d}",
        "Age_Group": random.choice(AGE_GROUPS),
        "Gender": random.choice(GENDERS),
        "Emergency_Level": random.choice(EMERGENCY_LEVELS),
        "Doctor": random.choice(DOCTORS),
    }

# Activity duration and timestamp generation

ACTIVITY_DURATION_RANGES = {
    "Registration": (5, 15),
    "Triage": (5, 20),
    "Doctor Consultation": (10, 30),
    "Investigation": (10, 25),
    "X-Ray": (15, 35),
    "Treatment": (15, 40),
    "Discharge": (5, 15),
}


EMERGENCY_WAIT_MULTIPLIER = {
    "Low": 1.30,
    "Medium": 1.00,
    "High": 0.75,
    "Critical": 0.50,
}


def generate_next_timestamp(current_timestamp, activity, emergency_level):
    """
    Generate the timestamp for the next activity.

    The generated duration varies by activity and emergency level.
    """

    min_minutes, max_minutes = ACTIVITY_DURATION_RANGES[activity]

    duration = random.randint(min_minutes, max_minutes)

    wait_multiplier = EMERGENCY_WAIT_MULTIPLIER[emergency_level]

    adjusted_duration = max(
        1,
        round(duration * wait_multiplier)
    )

    return current_timestamp + timedelta(minutes=adjusted_duration)

# Event record generation

def generate_patient_events(case_number, patient_number, start_timestamp):
    """
    Generate the complete event log for one synthetic patient.
    """

    patient = generate_patient_attributes(patient_number)

    pathway = select_pathway()

    activities = get_pathway_activities(pathway)

    case_id = f"C{case_number:04d}"

    events = []

    current_timestamp = start_timestamp

    for activity in activities:
        event = {
            "Case_ID": case_id,
            "Patient_ID": patient["Patient_ID"],
            "Activity_Name": activity,
            "Timestamp": current_timestamp,
            "Department": ACTIVITY_DEPARTMENTS[activity],
            "Doctor": patient["Doctor"],
            "Emergency_Level": patient["Emergency_Level"],
            "Age_Group": patient["Age_Group"],
            "Gender": patient["Gender"],
        }

        events.append(event)

        current_timestamp = generate_next_timestamp(
            current_timestamp,
            activity,
            patient["Emergency_Level"],
        )

    return events

# Full dataset generation

def generate_full_dataset():
    """
    Generate the complete synthetic EHR event log
    for all configured patients.
    """

    all_events = []

    base_date = datetime(2026, 1, 10, 9, 0, 0)

    for patient_number in range(1, NUM_PATIENTS + 1):

        # Spread patients across different starting times
        patient_start = base_date + timedelta(
            minutes=random.randint(0, 60 * 8)
        )

        events = generate_patient_events(
            case_number=patient_number,
            patient_number=patient_number,
            start_timestamp=patient_start,
        )

        all_events.extend(events)

    return pd.DataFrame(all_events)

# Main execution

if __name__ == "__main__":
    print("CareFlow EHR Generator")
    print("-" * 40)

    df = generate_full_dataset()

    output_path = "data/raw/ehr_event_log.csv"

    df.to_csv(
        output_path,
        index=False,
    )

    print(f"\nDataset saved to: {output_path}")

    print(f"Patients generated: {df['Patient_ID'].nunique()}")
    print(f"Cases generated: {df['Case_ID'].nunique()}")
    print(f"Events generated: {len(df)}")

    print("\nEvent log preview:")
    print(df.head(10).to_string(index=False))

    print("\nDataset generation completed successfully!")