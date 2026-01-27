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
from lib.stats import StatisticsComputer
from lib.load import load_data


@asynccontextmanager
async def lifespan(_: FastAPI):
    # TODO: Q3(a) - Implement lifespan startup logic
    pass
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
    # TODO: Q3(b) - Implement get_patients filter logic
    pass


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
