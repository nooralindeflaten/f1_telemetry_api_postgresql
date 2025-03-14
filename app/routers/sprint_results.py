# controllers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import SessionLocal, get_db
from typing import List

router = APIRouter()

# Dependency to get the database session

# Route to get all sprint results
@router.get("/sprint_results", response_model=List[schemas.SprintResultResponse])
def get_sprint_results(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(models.SprintResult).offset(skip).limit(limit).all()

# Route to get a specific sprint result by ID
@router.get("/sprint_results/{sprint_result_id}", response_model=schemas.SprintResultResponse)
def get_sprint_result(sprint_result_id: int, db: Session = Depends(get_db)):
    db_sprint_result = crud.get_sprint_result_by_id(db, sprint_result_id)
    if db_sprint_result is None:
        raise HTTPException(status_code=404, detail="Sprint Result not found")
    return db_sprint_result


# Route to create a new sprint result
@router.post("/sprint_results", response_model=schemas.SprintResultResponse)
def create_sprint_result(sprint_result: schemas.SprintResultCreate, db: Session = Depends(get_db)):
    return crud.create_sprint_result(db, sprint_result)
