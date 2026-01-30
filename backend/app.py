import uvicorn
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

import store
from custom_types.enums import AgeBand
from custom_types.models import (
    EnrichedPatient,
    BPStage,
    RiskLevel,
    DatasetStatistics,
)
from lib.extract import extract_patients
from lib.load import load_data


@asynccontextmanager
async def lifespan(_: FastAPI):
    patients = extract_patients()

    enriched_patients, patient_index, dataset_stats = load_data(patients)

    store.ENRICHED_PATIENTS = enriched_patients
    store.PATIENT_INDEX = patient_index
    store.DATASET_STATISTICS = dataset_stats

    yield

    store.reset_store()


app = FastAPI(
    title="Health Dashboard API",
    description="API for the health dashboard",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Health Dashboard API is running"}


@app.get(
    "/patients",
    response_model=list[EnrichedPatient],
    status_code=status.HTTP_200_OK,
)
def get_patients(
    risk_level: Optional[RiskLevel] = Query(None, description="Filter by risk level"),
    bp_stage: Optional[BPStage] = Query(None, description="Filter by BP stage"),
    age_band: Optional[AgeBand] = Query(None, description="Filter by age band"),
):
    patients = store.ENRICHED_PATIENTS or []

    # Filter by risk_level
    if risk_level:
        patients = [p for p in patients if p.risk_level == risk_level]

    # Filter by bp_stage
    if bp_stage:
        patients = [p for p in patients if p.bp_stage == bp_stage]

        # Filter by age_band
    if age_band:
            def get_band(p):
                age = p.age
                if 0 <= age <= 17:
                    return AgeBand.ZERO_TO_SEVENTEEN
                elif 18 <= age <= 39:
                    return AgeBand.EIGHTEEN_TO_THIRTY_NINE
                elif 40 <= age <= 64:
                    return AgeBand.FORTY_TO_SIXTY_FOUR
                else:
                    return AgeBand.SIXTY_FIVE_PLUS

            patients = [p for p in patients if get_band(p) == age_band]

    return patients

@app.get(
    "/patients/{patient_id}",
    response_model=EnrichedPatient,
    status_code=status.HTTP_200_OK,
)
def get_patient(patient_id: str):
    patient = store.PATIENT_INDEX.get(patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    return patient


@app.get(
    "/statistics",
    response_model=DatasetStatistics,
    status_code=status.HTTP_200_OK,
)
def get_statistics():
    if store.DATASET_STATISTICS is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Statistics not loaded",
        )

    return store.DATASET_STATISTICS


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
