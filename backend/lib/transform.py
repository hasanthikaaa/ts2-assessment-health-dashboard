from typing import Any, Dict

from custom_types.models import Patient, EnrichedPatient
from custom_types.enums import BPStage, RiskLevel


# TODO: Q1 - Implement the complete PatientTransformer class
class PatientTransformer:
    # TODO: Q1 - Implement derive_metrics method
    def derive_metrics(cls, patient: Patient, ctx: Dict[str, Any]) -> Dict[str, Any]:
        pass

    # TODO: Q1 - Implement classify_bp method
    def classify_bp(cls, patient: Patient, ctx: Dict[str, Any]) -> Dict[str, Any]:
        pass

    # TODO: Q1 - Implement apply_risk_rules method
    def apply_risk_rules(cls, patient: Patient, ctx: Dict[str, Any]) -> Dict[str, Any]:
        pass

    # TODO: Q1 - Implement prepare_enriched_patient method
    def prepare_enriched_patient(
        cls, patient: Patient, ctx: Dict[str, Any]
    ) -> EnrichedPatient:
        pass

    # TODO: Q1 - Implement enrich_patient method
    def enrich_patient(cls, patient: Patient) -> EnrichedPatient:
        pass
