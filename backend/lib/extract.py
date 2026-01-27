import csv
from typing import List

from custom_types.models import Patient


DATA_FILE = "data/clinical_data.csv"


def extract_patients() -> List[Patient]:
    patients: List[Patient] = []
    with open(DATA_FILE, mode="r", newline="", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            patient = Patient.model_validate(row)
            patients.append(patient)

    return patients
