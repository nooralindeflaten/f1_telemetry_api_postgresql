from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from typing import List

router = APIRouter()

@router.get("/seasons/", response_model=List[schemas.SeasonResponse])
def get_seasons(db: Session = Depends(get_db)):
    return db.query(models.Season).all()

@router.get("/seasons/{season_id}", response_model=schemas.SeasonResponse)
def get_season_id(season_id: int, db: Session = Depends(get_db)):
    return db.query(models.Season).filter(models.Season.seasonId == season_id).first()

@router.get("/seasons/{season_id}/races/", response_model=List[schemas.RaceResponse])
def get_season_id(season_id: int, db: Session = Depends(get_db)):
    races = crud.get_races_from_seasons(db, season_id)
    if races is None:
        raise HTTPException(status_code=404,detail="No races found")
    return races
