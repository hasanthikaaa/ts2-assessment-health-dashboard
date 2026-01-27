from .transform import PatientTransformer
from .stats import StatisticsComputer

from custom_types.models import Patient, EnrichedPatient, DatasetStatistics
from typing import Tuple, Dict, List


def load_data(
    patients: List[Patient],
) -> Tuple[List[EnrichedPatient], Dict[str, EnrichedPatient], DatasetStatistics]:
    enriched_patients: List[EnrichedPatient] = []
    patient_index: Dict[str, EnrichedPatient] = {}

    for patient in patients:
        enriched = PatientTransformer.enrich_patient(patient)
        enriched_patients.append(enriched)
        patient_index[enriched.patient_id] = enriched

    dataset_statistics = StatisticsComputer.compute_statistics(enriched_patients)

    return enriched_patients, patient_index, dataset_statistics


# store.ENRICHED_PATIENTS = enriched_patients
# store.PATIENT_INDEX = patient_index
# store.DATASET_STATISTICS = compute_statistics(enriched_patients)
