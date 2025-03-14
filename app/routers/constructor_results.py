from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal
from typing import List

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to get all constructor results
@router.get("/constructor_results", response_model=List[schemas.ConstructorResultResponse])
def get_constructor_results(db: Session = Depends(get_db)):
    return crud.get_constructor_results(db)

# Route to get a constructor result by ID
@router.get("/constructor_results/{result_id}", response_model=schemas.ConstructorResultResponse)
def get_constructor_result(result_id: int, db: Session = Depends(get_db)):
    db_constructor_result = crud.get_constructor_result_by_id(db, result_id)
    if db_constructor_result is None:
        raise HTTPException(status_code=404, detail="Constructor result not found")
    return db_constructor_result

# Route to create a new constructor result
@router.post("/constructor_results", response_model=schemas.ConstructorResultResponse)
def create_constructor_result(constructor_result: schemas.ConstructorResultCreate, db: Session = Depends(get_db)):
    return crud.create_constructor_result(db, constructor_result)