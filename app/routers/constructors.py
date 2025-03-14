# controllers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal, get_db
from typing import List


router = APIRouter()


# Route to get all constructors
@router.get("/constructors", response_model=List[schemas.ConstructorResponse])
def get_constructors(db: Session = Depends(get_db)):
    return crud.get_constructors(db)

# Route to get a constructor by ID
@router.get("/constructors/{constructor_id}", response_model=schemas.ConstructorResponse)
def get_constructor(constructor_id: int, db: Session = Depends(get_db)):
    db_constructor = crud.get_constructor_by_id(db, constructor_id)
    if db_constructor is None:
        raise HTTPException(status_code=404, detail="Constructor not found")
    return db_constructor

#Relationships
@router.get("/constructors/{constructor_id}/constructor_standings", response_model=List[schemas.ConstructorStandingResponse])
def get_constructor_const_stand(constructor_id: int, db: Session = Depends(get_db)):
    db_constructor_standings = crud.get_constructor_standings_by_constructor(db, constructor_id)
    if db_constructor_standings is None:
        raise HTTPException(status_code=404, detail="Constructor not found")
    return db_constructor_standings

@router.get("/constructors/{constructor_id}/constructor_results", response_model=List[schemas.ConstructorResultResponse])
def get_constructor_const_results(constructor_id: int, db: Session = Depends(get_db)):
    db_constructor_result = crud.get_constructor_results_by_constructor(db, constructor_id)
    if db_constructor_result is None:
        raise HTTPException(status_code=404, detail="Constructor not found")
    return db_constructor_result

@router.get("/constructors/{constructor_id}/results", response_model=List[schemas.ResultResponse])
def get_results_constructor(constructor_id: int, db: Session = Depends(get_db)):
    results = crud.get_results_from_constructor(db, constructor_id)
    if results is None:
        raise HTTPException(status_code=404, detail="Constructor not found")
    return results

@router.get("/constructors/{constructor_id}/qualifying", response_model=List[schemas.QualifyingResponse])
def get_constructor_qualifying(constructor_id: int, db: Session = Depends(get_db)):
    qualifying = crud.get_qualifying_constructor(db, constructor_id)
    if qualifying is None:
        raise HTTPException(status_code=404, detail="Constructor not found")
    return qualifying

@router.get("/constructors/{constructor_id}/sprint_results", response_model=List[schemas.SprintResultResponse])
def get_constructor_sprint(constructor_id: int, db: Session = Depends(get_db)):
    sprint_results = crud.get_constructor_sprint_results(db, constructor_id)
    if sprint_results is None:
        raise HTTPException(status_code=404, detail="Constructor sprint not found")
    return sprint_results

# Route to create a new constructor
@router.post("/constructors", response_model=schemas.ConstructorResponse)
def create_constructor(constructor: schemas.ConstructorCreate, db: Session = Depends(get_db)):
    return crud.create_constructor(db, constructor)
