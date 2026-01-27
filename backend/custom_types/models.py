from typing import Any, Optional, List, Dict
from pydantic import BaseModel, Field, field_validator

from .enums import Gender, BPStage, RiskLevel


class Patient(BaseModel):
    patient_id: str = Field(
        min_length=7, max_length=7, description="Unique patient identifier"
    )
    age: int = Field(..., ge=0, le=130, description="Age of the patient in years")
    gender: Gender = Field(..., description="Gender (Male/Female)")
    blood_pressure_systolic: int = Field(
        ge=50, le=260, description="Systolic BP (mmHg)"
    )
    blood_pressure_diastolic: int = Field(
        ge=30, le=180, description="Diastolic BP (mmHg)"
    )
    heart_rate: int = Field(ge=20, le=250, description="Heart rate (bpm)")
    respiratory_rate: int = Field(
        ..., ge=5, le=80, description="Respiratory rate (breaths per minute)."
    )
    body_temperature: float = Field(
        ..., ge=80.0, le=115.0, description="Body temperature (deg. F)"
    )
    oxygen_saturation: int = Field(
        ..., ge=0, le=100, description="Oxygen saturation (%)"
    )
    glucose_fasting: int = Field(
        ..., ge=20, le=800, description="Fasting blood glucose (mg/dL)"
    )
    cholesterol_total: int = Field(
        ..., ge=50, le=600, description="Total cholesterol (mg/dL)"
    )
    pain_score: int = Field(..., ge=0, le=10, description="Pain score (0 to 10)")
    diabetes: bool = Field(..., description="Whether patient has diabetes")
    smoker: bool = Field(..., description="Whether patient is a smoker")

    @field_validator("patient_id", mode="before")
    @classmethod
    def normalize_patient_id(cls, value: Any) -> str:
        return str(value).strip()

    @field_validator("diabetes", "smoker", mode="before")
    @classmethod
    def coerce_bool(cls, value: Any) -> bool:
        if value not in ["0", "1"]:
            raise ValueError("bool value is not 0/1")
        return value == "1"

    @field_validator(
        "age",
        "blood_pressure_systolic",
        "blood_pressure_diastolic",
        "heart_rate",
        "respiratory_rate",
        "oxygen_saturation",
        "glucose_fasting",
        "cholesterol_total",
        "pain_score",
        mode="before",
    )
    @classmethod
    def coerce_int(cls, value: Any) -> int:
        try:
            return int(value)
        except ValueError as e:
            raise ValueError(f"Expected an int value, got {value!r}") from e

    @field_validator("body_temperature", mode="before")
    @classmethod
    def coerce_temperature(cls, value: Any) -> float:
        try:
            return float(value)
        except ValueError as e:
            raise ValueError(f"Expected an float value, got {value!r}") from e


class EnrichedPatient(Patient):
    pulse_pressure: int = Field(
        ..., description="Pulse pressure (systolic - diastolic)"
    )
    mean_arterial_pressure: float = Field(
        ..., description="Mean arterial pressure (mmHg)"
    )
    bp_stage: BPStage = Field(..., description="Blood pressure stage classification")
    flags: List[str] = Field(default_factory=list, description="Clinical flags")
    risk_score: int = Field(..., ge=0, description="Calculated risk score")
    risk_level: RiskLevel = Field(..., description="Risk level (low/medium/high)")
    reasons: List[str] = Field(
        default_factory=list, description="Trace log of rules that fired"
    )


class Stats(BaseModel):
    mean: float = Field(..., description="Mean value")
    median: float = Field(..., description="Median value")
    std_dev: float = Field(..., description="Population standard deviation")


class AgeBandStats(BaseModel):
    blood_pressure_systolic: Optional[Stats] = Field(
        None, description="Statistics for systolic blood pressure"
    )
    heart_rate: Optional[Stats] = Field(None, description="Statistics for heart rate")
    glucose_fasting: Optional[Stats] = Field(
        None, description="Statistics for fasting glucose"
    )


class DatasetStatistics(BaseModel):
    total_patients: int = Field(..., ge=0, description="Total number of patients")
    age_bands: Dict[str, Optional[AgeBandStats]] = Field(
        ..., description="Statistics grouped by age band"
    )
