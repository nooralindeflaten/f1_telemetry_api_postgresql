# app/routers/drivers.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import (
    Driver, DriverBase, PitStopResponse,
    DriverCreate, DriverUpdate, DriverResponse, ResultResponse,
    QualifyingResponse, LapTimeResponse,
    DriverStandingResponse, SprintResultResponse, RaceResponse)
from app import crud, models
from app.database import get_db
from typing import List, Optional

router = APIRouter()

@router.post("/", response_model=Driver)
def create_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    db_driver = crud.create_driver(db=db, driver=driver)
    return db_driver

@router.put("/drivers/", response_model=List[DriverResponse])
def get_drivers(db: Session = Depends(get_db)):
    return crud.get_drivers(db)



@router.get("/drivers/{driver_id}", response_model=DriverResponse)
def read_driver(driver_id: int, db: Session = Depends(get_db)):
    db_driver = crud.get_driver_by_id(db,driver_id=driver_id)
    if db_driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return db_driver

@router.get("/drivers/{driver_id}/results", response_model=List[ResultResponse])
def read_driver_result(driver_id: int, db: Session = Depends(get_db)):
    db_results = crud.get_results_from_driver(db, driver_id)
    if db_results is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return db_results

@router.get("/drivers/{driver_id}/qualifying", response_model=List[QualifyingResponse])
def read_driver_qualifying(driver_id: int, db: Session = Depends(get_db)):
    qualifying = crud.get_qualifying_from_driver(db, driver_id)
    if qualifying is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return qualifying

@router.get("/drivers/{driver_id}/pit_stops", response_model=List[PitStopResponse])
def read_driver_pit_stops(driver_id: int, db: Session = Depends(get_db)):
    db_results = crud.get_pit_stops_from_driver(db, driver_id)
    if db_results is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return db_results

@router.get("/drivers/{driver_id}/lap_times", response_model=List[LapTimeResponse])
def read_driver_laps(driver_id: int, db: Session = Depends(get_db)):
    lap_times = crud.get_lap_times_from_driver(db, driver_id)
    if lap_times is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return lap_times

@router.get("/drivers/{driver_id}/driver_standings", response_model=List[DriverStandingResponse])
def read_driver_standings(driver_id: int, db: Session = Depends(get_db)):
    driver_standings = crud.get_driver_standings_from_driver(db, driver_id)
    if driver_standings is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver_standings

@router.get("/drivers/{driver_id}/sprint_results", response_model=List[SprintResultResponse])
def read_driver_sprint_results(driver_id: int, db: Session = Depends(get_db)):
    sprint_results = crud.get_sprint_results_from_driver(db, driver_id)
    if sprint_results is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return sprint_results


@router.get("/drivers/{driver_id}/races", response_model=List[RaceResponse])
def get_driver_races(driver_id: int, db: Session = Depends(get_db)):
    """Retrieve all races where the driver participated."""
    races = crud.get_races_by_driver_id(db, driver_id)

    if not races:
        raise HTTPException(status_code=404, detail="No races found for this driver")

    return races




@router.get("/drivers/{driver_id}/races/{race_id}/full_data/")
def get_driver_race_data(driver_id: int, race_id: int, db: Session = Depends(get_db)):
    """Fetches all relevant data for a driver in a specific race."""

    # Fetch driver info
    driver = db.query(models.Driver).filter(models.Driver.driverId == driver_id).first()
    if not driver:
        return {"error": "Driver not found"}

    # Fetch race info
    race = db.query(models.Race).filter(models.Race.raceId == race_id).first()
    if not race:
        return {"error": "Race not found"}

    # Fetch all related data
    result = db.query(models.Result).filter(models.Result.driverId == driver_id, models.Result.raceId == race_id).first()
    pit_stops = db.query(models.PitStop).filter(models.PitStop.driverId == driver_id, models.PitStop.raceId == race_id).all()
    lap_times = db.query(models.LapTime).filter(models.LapTime.driverId == driver_id, models.LapTime.raceId == race_id).all()
    qualifying = db.query(models.Qualifying).filter(models.Qualifying.driverId == driver_id, models.Qualifying.driverId == race_id).first()
    standings = db.query(models.DriverStanding).filter(models.DriverStanding.driverId == driver_id, models.DriverStanding.raceId == race_id).first()
    sprint_results = db.query(models.SprintResult).filter(models.SprintResult.driverId == driver_id, models.SprintResult.raceId == race_id).first()

    return {
        "driver": {
            "driverId": driver.driverId,
            "driverRef": driver.driverRef,
            "code": driver.code,
            "name": f"{driver.forename} {driver.surname}",
            "nationality": driver.nationality,
            "dob": driver.dob,
        },
        "race": {
            "id": race.raceId,
            "name": race.name,
            "seasonId": race.seasonId,
            "round": race.round,
            "circuit": race.circuitId,
        },
        "result": result,
        "pit_stops": pit_stops,
        "lap_times": lap_times,
        "qualifying": qualifying,
        "standings": standings,
        "sprint_results": sprint_results
    }


@router.put("/drivers/{driver_id}", response_model=Driver)
def update_driver(driver_id: int, driver: DriverUpdate, db: Session = Depends(get_db)):
    db_driver = crud.update_driver(db, driver_id, driver)
    if db_driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return db_driver

@router.delete("/drivers/{driver_id}")
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    result = crud.delete_driver(db, driver_id)
    if result is False:
        raise HTTPException(status_code=404, detail="Driver not found")
    return {"detail": "Driver deleted successfully"}
