from typing import Optional

from custom_types.models import EnrichedPatient, DatasetStatistics

ENRICHED_PATIENTS: list[EnrichedPatient] = []
PATIENT_INDEX: dict[str, EnrichedPatient] = {}
DATASET_STATISTICS: Optional[DatasetStatistics] = None


def reset_store():
    global ENRICHED_PATIENTS, PATIENT_INDEX, DATASET_STATISTICS
    ENRICHED_PATIENTS.clear()
    PATIENT_INDEX.clear()
    DATASET_STATISTICS = None
