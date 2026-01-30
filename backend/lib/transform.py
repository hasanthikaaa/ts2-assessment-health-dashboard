from typing import Any, Dict

from custom_types.models import Patient, EnrichedPatient
from custom_types.enums import BPStage, RiskLevel

class PatientTransformer:
    @classmethod
    def derive_metrics(cls, patient: Patient, ctx: Dict[str, Any]) -> Dict[str, Any]:
        # Pulse Pressure
        ctx["pulse_pressure"] = (
            patient.blood_pressure_systolic - patient.blood_pressure_diastolic
        )

        # Mean Arterial Pressure
        ctx["mean_arterial_pressure"] = (
            2 * patient.blood_pressure_diastolic + patient.blood_pressure_systolic
        ) / 3

        return ctx

    @classmethod
    def classify_bp(cls, patient: Patient, ctx: Dict[str, Any]) -> Dict[str, Any]:
        sbp = patient.blood_pressure_systolic
        dbp = patient.blood_pressure_diastolic

        if sbp >= 180 or dbp >= 120:
            bp_stage = BPStage.HYPERTENSIVE_CRISIS
        elif sbp >= 140 or dbp >= 90:
            bp_stage = BPStage.STAGE_2
        elif sbp >= 130 or dbp >= 80:
            bp_stage = BPStage.STAGE_1
        elif sbp >= 120:
            bp_stage = BPStage.ELEVATED
        else:
            bp_stage = BPStage.NORMAL

        ctx["bp_stage"] = bp_stage
        return ctx

    @classmethod
    def apply_risk_rules(cls, patient: Patient, ctx: Dict[str, Any]) -> Dict[str, Any]:
        score = ctx.get("score", 0)
        flags = ctx.get("flags", [])
        reasons = ctx.get("reasons", [])

        # Hypoxia
        if patient.oxygen_saturation < 92:
            flags.append("hypoxia")
            score += 30
            reasons.append("SpO2 < 92% - hypoxia risk (+30)")

        # Hypertension
        if (
            patient.blood_pressure_systolic >= 140
            or patient.blood_pressure_diastolic >= 90
        ):
            flags.append("hypertension")
            score += 15
            reasons.append("BP in hypertension range (+15)")

        # Diabetes
        if patient.diabetes:
            score += 10
            reasons.append("Diabetes present (+10)")

        # Smoker
        if patient.smoker:
            score += 5
            reasons.append("Smoker (+5)")

        ctx["score"] = score
        ctx["flags"] = flags
        ctx["reasons"] = reasons
        return ctx

    @classmethod
    def prepare_enriched_patient(
        cls, patient: Patient, ctx: Dict[str, Any]
    ) -> EnrichedPatient:
        risk_score = ctx["score"]

        # Risk level mapping
        if risk_score < 20:
            risk_level = RiskLevel.LOW
        elif risk_score < 40:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.HIGH

        patient_data = patient.model_dump()
        patient_data["smoker"] = "1" if patient.smoker else "0"
        patient_data["diabetes"] = "1" if patient.diabetes else "0"

        return EnrichedPatient(
            **patient_data,
            pulse_pressure=ctx["pulse_pressure"],
            mean_arterial_pressure=round(ctx["mean_arterial_pressure"], 2),
            bp_stage=ctx["bp_stage"],
            flags=ctx["flags"],
            risk_score=risk_score,
            risk_level=risk_level,
            reasons=ctx["reasons"],
        )

    @classmethod
    def enrich_patient(cls, patient: Patient) -> EnrichedPatient:
        ctx: Dict[str, Any] = {
            "score": 0,
            "flags": [],
            "reasons": [],
        }

        ctx = cls.derive_metrics(patient, ctx)
        ctx = cls.classify_bp(patient, ctx)
        ctx = cls.apply_risk_rules(patient, ctx)

        return cls.prepare_enriched_patient(patient, ctx)
