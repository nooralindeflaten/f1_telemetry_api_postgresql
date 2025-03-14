# controllers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal, get_db
from typing import List

router = APIRouter()


# Route to get all statuses
@router.get("/status", response_model=List[schemas.Status])
def get_statuses(db: Session = Depends(get_db)):
    return crud.get_statuses(db)

# Route to get a status by ID
@router.get("/status/{status_id}", response_model=schemas.StatusResponse)
def get_status_val(status_id: int, db: Session = Depends(get_db)):
    db_status = crud.get_status_by_id(db, status_id)
    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return db_status

# Route to get a status by ID
@router.get("/status/{status_id}/results/", response_model=List[schemas.ResultResponse])
def get_status_results(status_id: int, db: Session = Depends(get_db)):
    results = crud.get_results_from_status(db, status_id)
    if results is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return results

# Route to get a status by ID
@router.get("/status/{status_id}/sprint_results/", response_model=List[schemas.SprintResultResponse])
def get_status_results(status_id: int, db: Session = Depends(get_db)):
    sprint_results = crud.get_results_from_status(db, status_id)
    if sprint_results is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return sprint_results

# Route to create a new status
@router.post("/statuses", response_model=schemas.Status)
def create_status(status: schemas.StatusCreate, db: Session = Depends(get_db)):
    return crud.create_status(db, status)
