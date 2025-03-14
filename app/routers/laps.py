from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from typing import List

router = APIRouter()

@router.post("/lap_times/",response_model=schemas.LapTimeResponse)
def create_lap(lap_time: schemas.LapTimeCreate, db: Session = Depends(get_db)):
    return crud.create_lap_time(db,lap_time)

@router.get("/lap_times/", response_model=List[schemas.LapTimeResponse])
def get_all_lap_times(db: Session = Depends(get_db)):
    return crud.get_lap_times(db)

@router.get("/lap_times/{lap_id}", response_model=schemas.LapTimeResponse)
def get_lap_times_id(lap_id: int, db: Session = Depends(get_db)):
    db_result = crud.get_lap_time(db,lap_id)
    if db_result is None:
        raise HTTPException(status_code=404, detail="Lap not found")
    return db_result


@router.put("/lap_times/{lap_id}", response_model=schemas.LapTimeResponse)
def update_Lap(lap_id: int, LapUpdate: schemas.LapTimeUpdate, db: Session = Depends(get_db)):
    updated_Lap = crud.update_lap_time(db, lap_id, LapUpdate)
    if not updated_Lap:
        raise HTTPException(status_code=404, detail="Lap not found")
    return updated_Lap

@router.delete("/{lap_id}")
def delete_Lap(lap_id: int, db: Session = Depends(get_db)):
    deleted_lap = crud.delete_lap_time(db, lap_id)
    if not deleted_lap:
        raise HTTPException(status_code=404, detail="Lap not found")
    return {"message": "Lap deleted"}
