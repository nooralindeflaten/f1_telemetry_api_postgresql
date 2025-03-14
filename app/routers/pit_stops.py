# controllers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal, get_db
from typing import List


router = APIRouter()

# Route to get all pit stops
@router.get("/pit_stops", response_model=List[schemas.PitStopResponse])
def get_pit_stops(db: Session = Depends(get_db)):
    return crud.get_pit_stops(db)

# Route to get a pit stop by ID
@router.get("/pit_stops/{pit_stop_id}", response_model=schemas.PitStopResponse)
def get_pit_stop(pit_stop_id: int, db: Session = Depends(get_db)):
    db_pit_stop = crud.get_pit_stop_by_id(db, pit_stop_id)
    if db_pit_stop is None:
        raise HTTPException(status_code=404, detail="Pit stop not found")
    return db_pit_stop

# Route to get a pit stop by ID
@router.get("/pit_stops/{pit_stop_id}/lap_times/", response_model=schemas.LapTimeResponse)
def get_pit_stop(pit_stop_id: int, db: Session = Depends(get_db)):
    db_lap = crud.get_pit_stop_by_lap(db, pit_stop_id)
    if db_lap is None:
        raise HTTPException(status_code=404, detail="Pit stop not found")
    return db_lap

# Route to create a new pit stop
@router.post("/pit_stops", response_model=schemas.PitStopResponse)
def create_pit_stop(pit_stop: schemas.PitStopCreate, db: Session = Depends(get_db)):
    return crud.create_pit_stop(db, pit_stop)
