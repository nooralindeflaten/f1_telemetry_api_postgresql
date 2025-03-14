# controllers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal, get_db
from typing import List

router = APIRouter()


# Route to get all driver standings
@router.get("/driver_standings", response_model=List[schemas.DriverStandingResponse])
def get_driver_standings(db: Session = Depends(get_db)):
    return crud.get_driver_standings(db)

# Route to get a specific driver standing by ID
@router.get("/driver_standings/{standing_id}", response_model=schemas.DriverStandingResponse)
def get_driver_standing(standing_id: int, db: Session = Depends(get_db)):
    db_driver_standing = crud.get_driver_standing_by_id(db, standing_id)
    if db_driver_standing is None:
        raise HTTPException(status_code=404, detail="Driver Standing not found")
    return db_driver_standing

# Route to get all standings for a specific driver
@router.get("/drivers/{driver_id}/driver_standings", response_model=List[schemas.DriverStandingResponse])
def get_driver_standings_by_driver(driver_id: int, db: Session = Depends(get_db)):
    return crud.get_driver_standings_by_driver_id(db, driver_id)

# Route to create a new driver standing
@router.post("/driver_standings", response_model=schemas.DriverStandingResponse)
def create_driver_standing(driver_standing: schemas.DriverStandingCreate, db: Session = Depends(get_db)):
    return crud.create_driver_standing(db, driver_standing)
