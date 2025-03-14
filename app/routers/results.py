from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from typing import List, Optional

router = APIRouter()

@router.get("/results/", response_model=List[schemas.ResultResponse])
def get_results(db: Session = Depends(get_db)):
    return crud.get_results_all(db)

@router.get("/results/{result_id}", response_model=schemas.ResultResponse)
def get_results_id(result_id: int, db: Session = Depends(get_db)):
    db_result = crud.get_results_by_id(db,result_id)
    if db_result is None:
        raise HTTPException(status_code=404, detail="Result not found")
    return db_result



@router.get("/results", response_model=List[schemas.ResultResponse])
def get_filtered_results(
    db: Session = Depends(get_db),
    race_id: Optional[int] = None,
    driver_id: Optional[int] = None,
    constructor_id: Optional[int] = None,
    status_id: Optional[int] = None
):
    return crud.get_result_filtered(db, race_id=race_id, driver_id=driver_id, constructor_id=constructor_id, status_id=status_id)

