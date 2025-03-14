import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base
from app.models import (
    Constructor,
    Driver, Season, Circuit, Status, Race, Result, PitStop, LapTime, Qualifying, SprintResult,
    ConstructorResult, ConstructorStanding, DriverStanding
)
from datetime import datetime
from datetime import time

# Function to safely parse dates
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None  # Return None if invalid

def parse_time(time_str):
    try:
        return datetime.strptime(time_str,"%H:%M:%S").time()
    except (ValueError, TypeError):
        return None
# Load Drivers
def load_drivers(db: Session):
    try:
        drivers = pd.read_csv('/Users/nooralindeflaten/Downloads/f1_results/drivers.csv')

        driver_objs = []
        for _, row in drivers.iterrows():
            existing_driver = db.query(Driver).filter_by(driverId=row['driverId']).first()
            if existing_driver:
                continue  # Skip inserting if the driver already exists

            driver = Driver(
                driverId=row['driverId'],
                driverRef=(row["driverRef"]).strip(),
                number=int(row["number"]) if str(row["number"]).isdigit() else None,
                code=row["code"].strip() if row["code"] else None,
                forename=row["forename"].strip(),
                surname=row["surname"].strip(),
                dob=parse_date(row["dob"]),
                nationality=row["nationality"].strip() if row["nationality"] else None
            )
            driver_objs.append(driver)

        db.bulk_save_objects(driver_objs)
        db.commit()
        print("✅ Drivers data loaded successfully!")
    except Exception as e:
        db.rollback()  # Rollback transaction on error
        print(f"❌ Error loading drivers: {e}")


# Load Circuits
def load_circuits(db: Session):
    circuits = pd.read_csv('/Users/nooralindeflaten/Downloads/f1_results/circuits.csv')

    circuit_objs = [
        Circuit(
            circuitId=row["circuitId"],
            circuitRef=row["circuitRef"].strip(),
            name=row["name"].strip(),
            location=row["location"].strip() if row["location"] else None,
            country=row["country"].strip() if row["country"] else None,
            lat=row["lat"] if pd.notna(row["lat"]) else None,
            lng=row["lng"] if pd.notna(row["lng"]) else None,
            alt=row["alt"] if pd.notna(row["alt"]) else None,
        )
        for _, row in circuits.iterrows()
    ]

    db.bulk_save_objects(circuit_objs)
    db.commit()
    print("✅ Circuits data loaded successfully!")

# Load Constructors
def load_constructors(db: Session):
    constructors = pd.read_csv('/Users/nooralindeflaten/Downloads/f1_results/constructors.csv')

    constructor_objs = [
        Constructor(
            constructorId=row['constructorId'],
            constructorRef=row["constructorRef"].strip(),
            name=row["name"].strip(),
            nationality=row["nationality"].strip(),
        )
        for _, row in constructors.iterrows()
    ]

    db.bulk_save_objects(constructor_objs)
    db.commit()
    print("✅ Constructors data loaded successfully!")

# Load Seasons
def load_seasons(db: Session):
    seasons = pd.read_csv('/Users/nooralindeflaten/Downloads/f1_results/seasons.csv')

    # Start the season_id from 1
    season_objs = [
        Season(year=row['year']) for _, row in seasons.iterrows()
    ]

    db.bulk_save_objects(season_objs)
    db.commit()
    print("✅ Seasons data loaded with sequential IDs!")

# Load Status
def load_status(db: Session):
    status_df = pd.read_csv('/Users/nooralindeflaten/Downloads/f1_results/status.csv')

    status_objs = [Status(statusId=row['statusId'], status=row['status']) for _, row in status_df.iterrows()]

    db.bulk_save_objects(status_objs)
    db.commit()
    print("✅ Status data loaded successfully!")


def get_season_id(db: Session, year: int):
    season = db.query(Season).filter(Season.year == year).first()
    return season.seasonId if season else year

def load_races(db: Session):
    races = pd.read_csv('/Users/nooralindeflaten/Downloads/f1_results/races.csv')
    race_obj = [
        Race(
            raceId=row['raceId'],
            seasonId=get_season_id(db,row['year']),
            round=row['round'],
            circuitId=row['circuitId'],
            name=row['name'],
            date=parse_date(row['date']),
            time=parse_time(row['time']),
            fp1_date=parse_date(row['fp1_date']),
            fp1_time=parse_time(row['fp1_time']),
            fp2_date=parse_date(row['fp2_date']),
            fp2_time=parse_time(row['fp2_time']),
            fp3_date=parse_date(row['fp3_date']),
            fp3_time=parse_time(row['fp3_time']),
            quali_date=parse_date(row['quali_date']),
            quali_time=parse_time(row['quali_time']),
            sprint_date=parse_date(row['sprint_date']),
            sprint_time=parse_time(row['sprint_time']),
        )
        for _, row in races.iterrows()
    ]
    db.bulk_save_objects(race_obj)
    db.commit()
    print("✅ Race data loaded successfully!")


def load_results(db: Session):
    results = pd.read_csv('/Users/nooralindeflaten/Downloads/f1_results/results.csv')
    result_obj = [
        Result(
            resultId=row['resultId'],
            raceId=row['raceId'],
            driverId=row['driverId'],
            constructorId=row['constructorId'],
            number=int(row['number']) if str(row['number']).isdigit() else None,
            grid=int(row['grid']) if str(row['grid']).isdigit() else None,
            position=int(row['position']) if str(row['position']).isdigit() else None,
            positionText=row['positionText'],
            positionOrder=int(row['positionOrder']) if str(row['positionOrder']).isdigit() else None,
            points=float(row['points']) if str(row['points']).isdigit() else None,
            laps=int(row['laps']) if str(row['laps']).isdigit() else None,
            time=row['time'],
            milliseconds=int(row['milliseconds']) if str(row['milliseconds']).isdigit() else None,
            fastestLap=int(row['fastestLap']) if str(row['fastestLap']).isdigit() else None,
            rank=row['rank'] if str(row['rank']).isdigit() else None,
            fastestLapTime=row['fastestLapTime'],
            fastestLapSpeed=float(row['fastestLapSpeed']) if str(row['fastestLapSpeed']).isdigit() else None,
            statusId=row['statusId'],
        )
        for _, row in results.iterrows()
    ]
    db.bulk_save_objects(result_obj)
    db.commit()
    print("✅ Result data loaded successfully!")

def load_lap_times(db: Session):
    lap_times=pd.read_csv('/Users/nooralindeflaten/Downloads/f1_results/lap_times.csv')
    lap_obj = [
        LapTime(
            raceId=row['raceId'],
            driverId=row['driverId'],
            lap=int(row['lap']) if str(row['lap']).isdigit() else None,
            position=int(row['position']) if str(row['position']).isdigit() else None,
            time=row['time'],
            milliseconds=int(row['milliseconds']) if str(row['lap']).isdigit() else None,
        )
        for _, row in lap_times.iterrows()
    ]
    db.bulk_save_objects(lap_obj)
    db.commit()
    print("✅ Lap data loaded successfully!")

def get_lap_num(db: Session, race: int, driver: int, lap: int):
    try:
        lap_num = db.query(LapTime).filter(LapTime.raceId==race,LapTime.driverId==driver,LapTime.lap==lap).first()
        return lap_num.lapId if lap_num else None
    except (ValueError,TypeError):
        return None

def load_pit_stops(db: Session):
    pit_stops=pd.read_csv('/Users/nooralindeflaten/Downloads/f1_results/pit_stops.csv')
    pit_stop_obj = [
        PitStop(
            raceId=row['raceId'],
            driverId=row['driverId'],
            lapId=get_lap_num(db,row['raceId'],row['driverId'],row['lap']),
            stop=int(row['stop']) if str(row['stop']).isdigit() else None,
            lap=int(row['lap']) if str(row['lap']).isdigit() else None,
            time=parse_time(row['time']),
            duration=row['duration'],
            milliseconds=int(row['milliseconds']) if str(row['milliseconds']).isdigit() else None,
        )
        for _, row in pit_stops.iterrows()
    ]
    db.bulk_save_objects(pit_stop_obj)
    db.commit()
    print("✅ Lap data loaded successfully!")


def load_qualifying(db: Session):
    qualify =pd.read_csv('/Users/nooralindeflaten/Downloads/f1_results/qualifying.csv')
    quali_obj = [
        Qualifying(
            qualifyId=row['qualifyId'],
            raceId=row['raceId'],
            driverId=row['driverId'],
            constructorId=row['constructorId'],
            number=int(row['number']) if str(row['number']).isdigit() else None,
            position=int(row['position']) if str(row['position']).isdigit() else None,
            q1=row['q1'],
            q2=row['q2'],
            q3=row['q3'],
        )
        for _, row in qualify.iterrows()
    ]
    db.bulk_save_objects(quali_obj)
    db.commit()
    print("✅ quali data loaded successfully!")



def load_sprint(db: Session):
    sprint_results = pd.read_csv('/Users/nooralindeflaten/Downloads/f1_results/sprint_results.csv')
    sprint_obj = [
        SprintResult(
            sprintResultId=row['resultId'],
            raceId=row['raceId'],
            driverId=row['driverId'],
            constructorId=row['constructorId'],
            number=int(row['number']) if str(row['number']).isdigit() else None,
            grid=int(row['grid']) if str(row['grid']).isdigit() else None,
            position=int(row['position']) if str(row['position']).isdigit() else None,
            positionText=row['positionText'],
            positionOrder=int(row['positionOrder']) if str(row['positionOrder']).isdigit() else None,
            points=int(row['points']) if str(row['points']).isdigit() else None,
            laps=int(row['laps']) if str(row['laps']).isdigit() else None,
            time=row['time'],
            milliseconds=int(row['milliseconds']) if str(row['milliseconds']).isdigit() else None,
            fastestLap=int(row['fastestLap']) if str(row['fastestLap']).isdigit() else None,
            fastestLapTime=row['fastestLapTime'],
            statusId=row['statusId'],
        )
        for _, row in sprint_results.iterrows()
    ]
    db.bulk_save_objects(sprint_obj)
    db.commit()
    print("✅ Sprint result data loaded successfully!")


def load_constructor_results(db: Session):
    constructor_results = pd.read_csv('/Users/nooralindeflaten/Downloads/f1_results/constructor_results.csv')
    constructor_res_obj = [
        ConstructorResult(
            constructorResultsId=row['constructorResultsId'],
            raceId = row['raceId'],
            constructorId = row['constructorId'],
            points=int(row['points']) if str(row['points']).isdigit() else None,
            status=row['status'],
        )
        for _, row in constructor_results.iterrows()
    ]
    db.bulk_save_objects(constructor_res_obj)
    db.commit()
    print("✅ Constructor result data loaded successfully!")

def load_constructor_standings(db: Session):
    constructor_standings = pd.read_csv('/Users/nooralindeflaten/Downloads/f1_results/constructor_standings.csv')
    constructor_stand_obj = [
        ConstructorStanding(
            constructorStandingsId=row['constructorStandingsId'],
            raceId=row['raceId'],
            constructorId=row['constructorId'],
            points=int(row['points']) if str(row['points']).isdigit() else None,
            position=int(row['position']) if str(row['position']).isdigit() else None,
            positionText=row['positionText'],
            wins=row['wins'],
        )
        for _, row in constructor_standings.iterrows()
    ]
    db.bulk_save_objects(constructor_stand_obj)
    db.commit()
    print("✅ Constructor standings data loaded successfully!")

def load_driver_standings(db: Session):
    driver_standings = pd.read_csv('/Users/nooralindeflaten/Downloads/f1_results/driver_standings.csv')
    driver_stand_obj = [
        DriverStanding(
            driverStandingsId=row['driverStandingsId'],
            raceId=row['raceId'],
            driverId=row['driverId'],
            points=int(row['points']) if str(row['points']).isdigit() else None,
            position=int(row['position']) if str(row['position']).isdigit() else None,
            positionText=row['positionText'],
            wins=row['wins'],
        )
        for _, row in driver_standings.iterrows()
    ]
    db.bulk_save_objects(driver_stand_obj)
    db.commit()
    print("✅ Driver standings data loaded successfully!")

# Main function to run all loaders
def main():
    db = SessionLocal()

    try:
        #load_drivers(db)
        #load_circuits(db)  # Added this function call
        #load_constructors(db)
        #load_seasons(db)
        #load_status(db)
        #load_races(db)
        load_driver_standings(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
