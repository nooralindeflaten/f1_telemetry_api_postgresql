from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from typing import List, Optional

router = APIRouter()

@router.get("/races/", response_model=List[schemas.RaceResponse])
def get_all_races(db: Session = Depends(get_db)):
    return crud.get_races(db)

@router.get("/races/{race_id}", response_model=schemas.RaceResponse)
def get_races_id(race_id: int, db: Session = Depends(get_db)):
    db_result = db.query(models.Race).filter(models.Race.raceId == race_id).first()
    if db_result is None:
        raise HTTPException(status_code=404, detail="Race not found")
    return db_result


@router.get("/races/{race_id}/qualifying/", response_model=List[schemas.QualifyingResponse])
def get_race_qualify(race_id: int, db: Session = Depends(get_db)):
    qualifying = crud.get_qualifying_from_race(db,race_id)
    if qualifying is None:
        raise HTTPException(status_code=404, detail="Race not found")
    return qualifying

@router.get("/races/{race_id}/results/", response_model=List[schemas.ResultResponse])
def get_race_results(race_id: int, db: Session = Depends(get_db)):
    results = crud.get_results_from_race(db,race_id)
    if results is None:
        raise HTTPException(status_code=404, detail="Race not found")
    return results

@router.get("/races/{race_id}/sprint_races/", response_model=List[schemas.SprintResultResponse])
def get_race_sprint(race_id: int, db: Session = Depends(get_db)):
    sprint_races = crud.get_sprint_results_from_race(db,race_id)
    if sprint_races is None:
        raise HTTPException(status_code=404, detail="Race not found")
    return sprint_races

@router.get("/races/{race_id}/pit_stops/", response_model=List[schemas.PitStopResponse])
def get_race_pit(race_id: int, db: Session = Depends(get_db)):
    pit_stops = crud.get_pit_stops_from_race(db,race_id)
    if pit_stops is None:
        raise HTTPException(status_code=404, detail="Race not found")
    return pit_stops

@router.get("/races/{race_id}/lap_times/", response_model=List[schemas.LapTimeResponse])
def get_race_lap(race_id: int, db: Session = Depends(get_db)):
    lap_times = crud.get_laps_from_race(db,race_id)
    if lap_times is None:
        raise HTTPException(status_code=404, detail="Race not found")
    return lap_times

@router.get("/races/{race_id}/driver_standings/", response_model=List[schemas.DriverStandingResponse])
def get_race_driverStand(race_id: int, db: Session = Depends(get_db)):
    driver_stands = crud.get_driver_standings_from_race(db,race_id)
    if driver_stands is None:
        raise HTTPException(status_code=404, detail="Race not found")
    return driver_stands

@router.get("/races/{race_id}/constructor_results/", response_model=List[schemas.ConstructorResultResponse])
def get_race_const_res(race_id: int, db: Session = Depends(get_db)):
    constructor_result = crud.get_constructor_results_from_race(db,race_id)
    if constructor_result is None:
        raise HTTPException(status_code=404, detail="Race for constructor result not found")
    return constructor_result

@router.get("/races/{race_id}/constructor_standings/", response_model=List[schemas.ConstructorStandingResponse])
def get_race_const_stand(race_id: int, db: Session = Depends(get_db)):
    constructor_standings = crud.get_constructor_standings_from_race(db,race_id)
    if constructor_standings is None:
        raise HTTPException(status_code=404, detail="Race for constructor result not found")
    return constructor_standings


