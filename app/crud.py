from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import schemas
from app.models import (
    Constructor,
    Driver, Season, Circuit, Status, Race, Result, PitStop, LapTime, Qualifying, SprintResult,
    ConstructorResult, ConstructorStanding, DriverStanding
)
from typing import Optional

# --------------- DRIVER ---------------
def get_drivers(db: Session):
    return db.query(Driver).all()

def get_driver_by_id(db: Session, driver_id: int):
    return db.query(Driver).filter(Driver.driverId == driver_id).first()

def create_driver(db: Session, driver_data: dict):
    driver = Driver(**driver_data)
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver

def update_driver(db: Session, driver_id: int, update_data: dict):
    driver = db.query(Driver).filter(Driver.driverId == driver_id).first()
    if not driver:
        return None
    for key, value in update_data.items():
        setattr(driver, key, value)
    db.commit()
    db.refresh(driver)
    return driver

def delete_driver(db: Session, driver_id: int):
    driver = db.query(Driver).filter(Driver.driverId == driver_id).first()
    if not driver:
        return None
    db.delete(driver)
    db.commit()
    return driver

def get_driver_by_value(db: Session, driver_value: str):
    """Retrieve a driver by driverRef, driverId, code, or full name."""
    return db.query(Driver).filter(
        or_(
            Driver.driverId == driver_value,
            Driver.driverRef == driver_value,
            Driver.code == driver_value,
            (Driver.forename + "%20" + Driver.surname) == driver_value
        )
    ).first()

def get_driver_by_ref(db: Session, driver_ref: str):
    return db.query(Driver).filter(Driver.driverRef == driver_ref).first()

def get_results_from_driver(db: Session, driver_id: int):
    return db.query(Driver).filter(Driver.driverId==driver_id).first().results

def get_qualifying_from_driver(db: Session, driver_id: int):
    return db.query(Driver).filter(Driver.driverId==driver_id).first().qualifying

def get_pit_stops_from_driver(db: Session, driver_id: int):
    return db.query(Driver).filter(Driver.driverId==driver_id).first().pit_stops

def get_lap_times_from_driver(db: Session, driver_id: int):
    return db.query(Driver).filter(Driver.driverId==driver_id).first().lap_times

def get_driver_standings_from_driver(db: Session, driver_id:int):
    return db.query(Driver).filter(Driver.driverId==driver_id).first().driver_standings

def get_sprint_results_from_driver(db: Session, driver_id: int):
    return db.query(Driver).filter(Driver.driverId==driver_id).first().sprint_results

#Trying to get race from results
def get_races_by_driver_id(db: Session, driver_id: int):
    """Get all unique races where the driver has participated (via results)."""
    return (
        db.query(Race)
        .join(Result)
        .filter(Result.driverId == driver_id)
        .distinct()
        .all()
    )


#----------------------------Driver Standings-----------------------------
def get_driver_standings(db: Session):
    return db.query(DriverStanding).all()

def get_driver_standing_by_id(db: Session, standing_id: int):
    return db.query(DriverStanding).filter(DriverStanding.driverStandingsId == standing_id).first()


def create_driver_standing(db: Session, driver_standing: schemas.DriverStandingCreate):
    db_driver_standing = DriverStanding(
                raceId=driver_standing.raceId,
                driverId=driver_standing.driverId,
                points=driver_standing.points,
                position=driver_standing.position,
                positionText=driver_standing.positionText,
                wins=driver_standing.wins
                )
    db.add(db_driver_standing)
    db.commit()
    db.refresh(db_driver_standing)
    return db_driver_standing

# --------------- CIRCUIT ---------------
def get_circuits(db: Session):
    return db.query(Circuit).all()

def get_circuit(db: Session, circuit_id: int):
    return db.query(Circuit).filter(Circuit.circuitId == circuit_id).first()

def create_circuit(db: Session, circuit_data: dict):
    circuit = Circuit(**circuit_data)
    db.add(circuit)
    db.commit()
    db.refresh(circuit)
    return circuit

def update_circuit(db: Session, circuit_id: int, update_data: dict):
    circuit = db.query(Circuit).filter(Circuit.circuitId == circuit_id).first()
    if not circuit:
        return None
    for key, value in update_data.items():
        setattr(circuit, key, value)
    db.commit()
    db.refresh(circuit)
    return circuit

def delete_circuit(db: Session, circuit_id: int):
    circuit = db.query(Circuit).filter(Circuit.circuitId == circuit_id).first()
    if not circuit:
        return None
    db.delete(circuit)
    db.commit()
    return circuit


#Relationship functions
def get_races_on_circuit(db: Session, circuit_id):
    return db.query(Circuit).filter(Circuit.circuitId==circuit_id).first().races

# --------------- RACE ---------------
def get_races(db: Session):
    return db.query(Race).all()

def get_race(db: Session, race_id: int):
    return db.query(Race).filter(Race.raceId == race_id).first()

def create_race(db: Session, race_data: dict):
    race = Race(**race_data)
    db.add(race)
    db.commit()
    db.refresh(race)
    return race

def update_race(db: Session, race_id: int, update_data: dict):
    race = db.query(Race).filter(Race.raceId == race_id).first()
    if not race:
        return None
    for key, value in update_data.items():
        setattr(race, key, value)
    db.commit()
    db.refresh(race)
    return race

def delete_race(db: Session, race_id: int):
    race = db.query(Race).filter(Race.raceId == race_id).first()
    if not race:
        return None
    db.delete(race)
    db.commit()
    return race


#Relationships

def get_results_from_race(db: Session, race_id: int):
    return db.query(Race).filter(Race.raceId == race_id).first().results

def get_sprint_results_from_race(db: Session, race_id: int):
    return db.query(Race).filter(Race.raceId == race_id).first().sprint_results

def get_qualifying_from_race(db: Session, race_id: int):
    return db.query(Race).filter(Race.raceId == race_id).first().qualifying

def get_pit_stops_from_race(db: Session, race_id: int):
    return db.query(Race).filter(Race.raceId == race_id).first().pit_stops

def get_laps_from_race(db: Session, race_id: int):
    return db.query(Race).filter(Race.raceId == race_id).first().lap_times

def get_driver_standings_from_race(db: Session, race_id: int):
    return db.query(Race).filter(Race.raceId == race_id).first().driver_standings

def get_constructor_results_from_race(db: Session, race_id: int):
    return db.query(Race).filter(Race.raceId == race_id).first().constructor_results

def get_constructor_standings_from_race(db: Session, race_id: int):
    return db.query(Race).filter(Race.raceId == race_id).first().constructor_standings

# --------------- SEASON ---------------
def get_seasons(db: Session):
    return db.query(Season).all()


def create_season(db: Session, season_data: dict):
    season = Season(**season_data)
    db.add(season)
    db.commit()
    db.refresh(season)
    return season

def update_season(db: Session, season_id: int, update_data: dict):
    season = db.query(Season).filter(Season.seasonId == season_id).first()
    if not season:
        return None
    for key, value in update_data.items():
        setattr(season, key, value)
    db.commit()
    db.refresh(season)
    return season

def delete_season(db: Session, season_id: int):
    season = db.query(Season).filter(Season.seasonId == season_id).first()
    if not season:
        return None
    db.delete(season)
    db.commit()
    return season

def get_races_from_seasons(db: Session, season_id):
    return db.query(Season).filter(Season.seasonId==season_id).first().races


# Repeat for other tables...

# --------------- LAP TIME ---------------
def get_lap_times(db: Session):
    return db.query(LapTime).all()

def get_lap_time(db: Session, lap_id: int):
    return db.query(LapTime).filter(LapTime.lapId == lap_id).first()

def create_lap_time(db: Session, lap_data: dict):
    lap_time = LapTime(**lap_data)
    db.add(lap_time)
    db.commit()
    db.refresh(lap_time)
    return lap_time

def update_lap_time(db: Session, lap_id: int, update_data: dict):
    lap_time = db.query(LapTime).filter(LapTime.lapId == lap_id).first()
    if not lap_time:
        return None
    for key, value in update_data.items():
        setattr(lap_time, key, value)
    db.commit()
    db.refresh(lap_time)
    return lap_time

def delete_lap_time(db: Session, lap_id: int):
    lap_time = db.query(LapTime).filter(LapTime.lapId == lap_id).first()
    if not lap_time:
        return None
    db.delete(lap_time)
    db.commit()
    return lap_time


# --------------------------- Results ---------------------------------------
def get_result_filtered(db: Session, race_id: Optional[int] = None,
                        driver_id: Optional[int] = None,
                        constructor_id: Optional[int] = None,
                        status_id: Optional[int] = None):
    query = db.query(Result)

    if race_id:
        query = query.filter(Result.raceId == race_id)
    if driver_id:
        query = query.join(Driver, Result.driverId == Driver.driverId).filter(Driver.driverId == driver_id)
    if constructor_id:
        query = query.join(Constructor, Result.constructorId == Constructor.constructorId).filter(Constructor.constructorId == constructor_id)
    if status_id:
        query = query.join(Status, Result.statusId == Status.statusId).filter(Status.statusId == status_id)

    return query.all()


def get_results_all(db: Session):
    return db.query(Result).all()

def get_results_by_id(db: Session, result_id: int):
    return db.query(Result).filter(Result.resultId == result_id).first()

def get_results_for_race(db: Session, race_id: int):
    return db.query(Result).filter(Result.raceId == race_id).all()


def get_result_by_driver(db: Session, driver_id: int):
    return db.query(Result).join(Driver).filter(Driver.driverId == driver_id).all()

# -------------------------------- Sprint Results -------------------------------------------------------
def get_sprint_results(db: Session):
    return db.query(SprintResult).all()

def get_sprint_result_by_id(db: Session, sprint_result_id: int):
    return db.query(SprintResult).filter(SprintResult.sprintResultId == sprint_result_id).first()

def get_sprint_results_by_race_id(db: Session, race_id: int):
    return db.query(SprintResult).filter(SprintResult.raceId == race_id).all()

def get_sprint_results_by_driver_id(db: Session, driver_id: int):
    return db.query(SprintResult).filter(SprintResult.driverId == driver_id).all()

def create_sprint_result(db: Session, sprint_result: schemas.SprintResultCreate):
    db_sprint_result = SprintResult(
        raceId = sprint_result.raceId,
        driverId=sprint_result.driverId,
        constructorId=sprint_result.constructorId,
        number=sprint_result.number,
        grid=sprint_result.grid,
        position=sprint_result.position,
        positionText=sprint_result.positionText,
        positionOrder=sprint_result.positionOrder,
        points=sprint_result.points,
        laps=sprint_result.laps,
        time=sprint_result.time,
        milliseconds=sprint_result.milliseconds,
        fastestLap=sprint_result.fastestLap,
        fastestLapTime=sprint_result.fastestLapTime,
        statusId=sprint_result.statusId
    )
    db.add(db_sprint_result)
    db.commit()
    db.refresh(db_sprint_result)
    return db_sprint_result



#-----------------------------------Qualifying--------------------------------------------------
def create_qualifying(db: Session, qualifying: schemas.QualifyingBase):
    db_qualifying = Qualifying(**qualifying)
    db.add(db_qualifying)
    db.commit()
    db.refresh(db_qualifying)
    return db_qualifying


def update_qualifying_position(db: Session, qualifying_id: int, new_position: int):
    qualifying = db.query(Qualifying).filter(Qualifying.qualifyId == qualifying_id).first()
    if qualifying:
        qualifying.position = new_position
        db.commit()
        db.refresh(qualifying)
        return qualifying
    return None


def delete_qualifying(db: Session, qualifying_id: int):
    qualifying = db.query(Qualifying).filter(Qualifying.qualifyId == qualifying_id).first()
    if qualifying:
        db.delete(qualifying)
        db.commit()
        return True
    return False

def get_qualifying_id(db: Session, qualify_id: int):
    return db.query(Qualifying).filter(Qualifying.qualifyId==qualify_id).first()

# --------------------------------Status----------------------------------------
def get_statuses(db: Session):
    return db.query(Status).all()

def get_status_by_id(db: Session, status_id: int):
    return db.query(Status).filter(Status.statusId == status_id).first()

def create_status(db: Session, status: schemas.StatusCreate):
    db_status = Status(status=status.status)
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

#relationships
def get_results_from_status(db: Session, status_id: int):
    return db.query(Status).filter(Status.statusId==status_id).first().results

def get_sprint_results_from_status(db: Session, status_id: int):
    return db.query(Status).filter(Status.statusId==status_id).first().sprint_results



#-------------------------------- Pit stops ---------------------------------------
def get_pit_stops(db: Session):
    return db.query(PitStop).all()

def get_pit_stop_by_id(db: Session, pit_stop_id: int):
    return db.query(PitStop).filter(PitStop.pitStopId == pit_stop_id).first()

def get_pit_stop_by_lap(db: Session, pit_stop_id: int):
    return db.query(PitStop).filter(PitStop.pitStopId == pit_stop_id).first().lap_time

def create_pit_stop(db: Session, pit_stop: schemas.PitStopCreate):
    db_pit_stop = PitStop(
        raceId=pit_stop.raceId,
        driverId=pit_stop.driverId,
        stop=pit_stop.stop,
        lap=pit_stop.lapId,
        time=pit_stop.time
    )
    db.add(db_pit_stop)
    db.commit()
    db.refresh(db_pit_stop)
    return db_pit_stop



#-----------------------------ConstructorStandings------------------------------
# services.py

from sqlalchemy.orm import Session
from app.models import ConstructorStanding

def get_constructor_standings(db: Session):
    return db.query(ConstructorStanding).all()

def get_constructor_standing_by_id(db: Session, standing_id: int):
    return db.query(ConstructorStanding).filter(ConstructorStanding.constructorStandingsId == standing_id).first()

def create_constructor_standing(db: Session, constructor_standing: schemas.ConstructorStandingCreate):
    db_constructor_standing = ConstructorStanding(
        raceId=constructor_standing.raceId,
        constructorId=constructor_standing.constructorId,
        points=constructor_standing.points,
        position=constructor_standing.position,
        positionText=constructor_standing.positionText,
        wins=constructor_standing.wins
    )
    db.add(db_constructor_standing)
    db.commit()
    db.refresh(db_constructor_standing)
    return db_constructor_standing


#-----------------------------ConstructorResults------------------------------

def get_constructor_results(db: Session):
    return db.query(ConstructorResult).all()

def get_constructor_result_by_id(db: Session, result_id: int):
    return db.query(ConstructorResult).filter(ConstructorResult.constructorResultsId == result_id).first()

def create_constructor_result(db: Session, constructor_result: schemas.ConstructorResultCreate):
    db_constructor_result = ConstructorResult(
        raceId=constructor_result.raceId,
        constructorId=constructor_result.constructorId,
        points=constructor_result.points,
        status=constructor_result.status
    )
    db.add(db_constructor_result)
    db.commit()
    db.refresh(db_constructor_result)
    return db_constructor_result


#----------------------------Constructor-----------------------------------------

def get_constructors(db: Session):
    return db.query(Constructor).all()

def get_constructor_by_id(db: Session, constructor_id: int):
    return db.query(Constructor).filter(Constructor.constructorId == constructor_id).first()

def create_constructor(db: Session, constructor: schemas.ConstructorCreate):
    db_constructor = Constructor(
        constructorRef=constructor.constructorRef,
        name=constructor.name,
        nationality=constructor.nationality
    )
    db.add(db_constructor)
    db.commit()
    db.refresh(db_constructor)
    return db_constructor

# Relationships

def get_constructor_standings_by_constructor(db: Session, constructor_id):
    return db.query(Constructor).filter(Constructor.constructorId==constructor_id).first().constructor_standings

def get_constructor_results_by_constructor(db: Session, constructor_id):
    return db.query(Constructor).filter(Constructor.constructorId==constructor_id).first().constructor_results

def get_results_from_constructor(db: Session, constructor_id):
    return db.query(Constructor).filter(Constructor.constructorId==constructor_id).first().results

def get_qualifying_constructor(db: Session, constructor_id):
    return db.query(Constructor).filter(Constructor.constructorId==constructor_id).first().qualifying

def get_constructor_sprint_results(db: Session, constructor_id):
    return db.query(Constructor).filter(Constructor.constructorId==constructor_id).first().sprint_results



