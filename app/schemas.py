from pydantic import BaseModel
from typing import List, Optional
import datetime as dt
from datetime import date, time


# Base schema with common fields
class IDBase(BaseModel):
    id: int

    class Config:
        from_attributes = True


class CircuitBase(BaseModel):
    circuitId: int
    circuitRef: str
    name: str
    location: Optional[str]
    country: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    alt: Optional[int]

class CircuitResponse(BaseModel):
    circuitId: int
    circuitRef: str
    name: str
    location: Optional[str]
    country: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    alt: Optional[int]

    class Config:
        from_attributes = True

class CircuitCreate(CircuitBase):
    pass


class CircuitUpdate(BaseModel):
    circuitRef: str
    name: str
    location: Optional[str]
    country: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    alt: Optional[int]

    class Config:
        from_attributes = True

class Circuit(CircuitBase):
    circuitId: int
    races: List["Race"] = []  # Circular reference to Race

    class Config:
        from_attributes = True


class PitStopBase(BaseModel):
    pitStopId: int
    raceId: int
    driverId: int
    lapId: int  # Ensure it references LapTime correctly
    stop: Optional[int]
    lap: int
    time: Optional[time]
    duration: Optional[str]
    milliseconds: Optional[int]

class PitStopResponse(BaseModel):
    pitStopId: int
    raceId: int
    driverId: int
    lapId: int  # Ensure it references LapTime correctly
    stop: Optional[int]
    lap: int
    time: Optional[time]
    duration: Optional[str]
    milliseconds: Optional[int]

    class Config:
        from_attributes = True

class PitStopCreate(PitStopBase):
    pass


class PitStop(PitStopBase, IDBase):
    race: "Race"
    driver: "Driver"
    lap_time: "LapTime"  # Added relationship to LapTime

    class Config:
        from_attributes = True


class QualifyingBase(BaseModel):
    raceId: int
    driverId: int
    constructorId: int
    number: Optional[int]
    position: Optional[int]
    q1: Optional[str]
    q2: Optional[str]
    q3: Optional[str]


class QualifyingCreate(QualifyingBase):
    pass



class QualifyingResponse(BaseModel):
    qualifyId: int
    raceId: int
    driverId: int
    constructorId: int
    number: Optional[int]
    position: Optional[int]
    q1: Optional[str]
    q2: Optional[str]
    q3: Optional[str]
    class Config:
        from_attributes = True

class Qualifying(QualifyingBase):
    qualifyId: int
    race: "Race"
    constructor: "Constructor"
    driver: "Driver"

    class Config:
        from_attributes = True


class RaceBase(BaseModel):
    seasonId: int
    round: int
    circuitId: int
    name: str
    date: Optional[date]
    time: Optional[time]
    fp1_date: Optional[dt.date]
    fp1_time: Optional[dt.time]
    fp2_date: Optional[dt.date]
    fp2_time: Optional[dt.time]
    fp3_date: Optional[dt.date]
    fp3_time: Optional[dt.time]
    quali_date: Optional[dt.date]
    quali_time: Optional[dt.time]
    sprint_date: Optional[dt.date]
    sprint_time: Optional[dt.time]


class RaceCreate(RaceBase):
    pass


class Race(RaceBase):
    raceId: int
    #Many races can have the same season and circuit
    season: "Season"
    circuit: "Circuit"
    #A single raceId can occur multiple times in these
    qualifying: List["Qualifying"] = []
    results: List["Result"] = []
    sprint_results: List["SprintResult"] = []
    pit_stops: List["PitStop"] = []
    lap_times: List["LapTime"] = []
    driver_standings: List["DriverStanding"] = []
    constructor_standings: List["ConstructorStanding"] = []
    constructor_results: List["ConstructorResult"] = []

    class Config:
        from_attributes = True

class RaceResponse(BaseModel):
    raceId: int
    seasonId: int
    round: int
    circuitId: int
    name: str
    date: Optional[date]
    time: Optional[time]
    fp1_date: Optional[dt.date]
    fp1_time: Optional[dt.time]
    fp2_date: Optional[dt.date]
    fp2_time: Optional[dt.time]
    fp3_date: Optional[dt.date]
    fp3_time: Optional[dt.time]
    quali_date: Optional[dt.date]
    quali_time: Optional[dt.time]
    sprint_date: Optional[dt.date]
    sprint_time: Optional[dt.time]

    class Config:
        from_attributes = True


class ConstructorBase(BaseModel):
    constructorRef: str
    name: str
    nationality: Optional[str]

class ConstructorResponse(BaseModel):
    constructorId: int
    constructorRef: str
    name: str
    nationality: Optional[str]
    class Config:
        from_attributes = True

class ConstructorCreate(ConstructorBase):
    pass


class Constructor(ConstructorBase):
    constructorId: int
    constructor_results: List["ConstructorResult"] = []
    constructor_standings: List["ConstructorStanding"] = []
    results: List["Result"] = []
    qualifying: List[Qualifying] = []
    sprint_results: List["SprintResult"] = []

    class Config:
        from_attributes = True


class DriverBase(BaseModel):
    driverRef: str
    number: Optional[int] = None
    code: Optional[str] = None
    forename: str
    surname: str
    dob: Optional[date]
    nationality: Optional[str]

class DriverResponse(BaseModel):
    driverId: int
    driverRef: str
    number: Optional[int] = None
    code: Optional[str] = None
    forename: str
    surname: str
    dob: Optional[date]
    nationality: Optional[str]

    class Config:
        from_attributes = True

class DriverCreate(DriverBase):
    pass

# 🔄 Schema for updating a driver (all fields optional)
class DriverUpdate(BaseModel):
    driverRef: Optional[str] = None
    forename: Optional[str] = None
    surname: Optional[str] = None
    dob: Optional[date] = None
    nationality: Optional[str] = None
    number: Optional[int] = None
    code: Optional[str] = None

    class Config:
        from_attributes = True  # Allows conversion from ORM models

class Driver(DriverBase):
    driverId: int
    # A single driver can have multiple
    results: List["Result"] = []
    qualifying: List["Qualifying"] = []
    pit_stops: List["PitStop"] = []
    lap_times: List["LapTime"] = []
    driver_standings: List["DriverStanding"] = []
    sprint_results: List["SprintResult"] = []

    class Config:
        from_attributes = True


class ConstructorResultBase(BaseModel):
    raceId: int
    constructorId: int
    points: Optional[int]
    status: Optional[str]
    class Config:
        from_attributes = True
class ConstructorResultResponse(BaseModel):
    constructorResultsId: int
    raceId: int
    constructorId: int
    points: Optional[int]
    status: Optional[str]
    class Config:
        from_attributes = True

class ConstructorResultCreate(ConstructorResultBase):
    pass


class ConstructorResult(ConstructorResultBase):
    constructorResultsId: int
    #Many constructorResults can contain the same race or circuit
    race: "Race"
    constructor: "Constructor"
    class Config:
        from_attributes = True


class ConstructorStandingBase(BaseModel):
    raceId: int
    constructorId: int
    points: int
    position: int
    positionText: str
    wins: int

class ConstructorStandingResponse(BaseModel):
    constructorStandingsId: int
    raceId: int
    constructorId: int
    points: int
    position: int
    positionText: str
    wins: int
    class Config:
        from_attributes = True
class ConstructorStandingCreate(ConstructorStandingBase):
    pass


class ConstructorStanding(ConstructorStandingBase):
    constructorStandingsId: int
    race: "Race"
    constructor: "Constructor"

    class Config:
        from_attributes = True



class DriverStandingBase(BaseModel):
    raceId: int
    driverId: int
    points: int
    position: int
    positionText: str
    wins: int

class DriverStandingResponse(BaseModel):
    driverStandingsId: int
    raceId: int
    driverId: int
    points: int
    position: Optional[int]
    positionText: Optional[str]
    wins: Optional[int]
    class Config:
        from_attributes = True

class DriverStandingCreate(DriverStandingBase):
    pass


class DriverStanding(DriverStandingBase):
    driverStandingsId: int
    race: "Race"
    driver: "Driver"

    class Config:
        from_attributes = True

class LapTimeBase(BaseModel):
    lapId: int  # Added lapId to match the model
    raceId: int
    driverId: int
    lap: int
    position: int
    time: str
    milliseconds: int


class LapTimeCreate(LapTimeBase):
    pass


class LapTime(LapTimeBase):
    lapId: int
    race: "Race"
    driver: "Driver"
    pit_stop: "PitStop"  # Added relationship to PitStop

    class Config:
        from_attributes = True

class LapTimeResponse(BaseModel):
    lapId: int  # Added lapId to match the model
    raceId: int
    driverId: int
    lap: int
    position: int
    time: str
    milliseconds: int

    class Config:
        from_attributes = True

class LapTimeUpdate(BaseModel):
    lapId: int  # Added lapId to match the model
    raceId: Optional[int] = None
    driverId: Optional[int] = None
    lap: Optional[int] = None
    position: Optional[int] = None
    time: Optional[str] = None
    milliseconds: Optional[int] = None

    class Config:
        from_attributes = True


class ResultBase(BaseModel):
    raceId: int
    driverId: int
    constructorId: int
    number: Optional[int]
    grid: Optional[int]
    position: Optional[int]
    positionText: Optional[str]
    positionOrder: Optional[int]
    points: Optional[int]
    laps: Optional[int]
    time: Optional[str]
    milliseconds: Optional[int]
    fastestLap: Optional[int]
    rank: Optional[int]
    fastestLapTime: Optional[str]
    fastestLapSpeed: Optional[float]
    statusId: Optional[int]


class ResultCreate(ResultBase):
    pass

class ResultResponse(BaseModel):
    raceId: int
    driverId: int
    constructorId: int
    number: Optional[int]
    grid: Optional[int]
    position: Optional[int]
    positionText: Optional[str]
    positionOrder: Optional[int]
    points: Optional[int] = None
    laps: Optional[int]
    time: Optional[str]
    milliseconds: Optional[int]
    fastestLap: Optional[int]
    rank: Optional[int]
    fastestLapTime: Optional[str]
    fastestLapSpeed: Optional[float]
    statusId: Optional[int]

    class Config:
        from_attributes = True

class Result(ResultBase):
    resultId: int
    race: "Race"
    driver: "Driver"
    constructor: "Constructor"
    status: "Status"

    class Config:
        from_attributes = True


class SeasonBase(BaseModel):
    year: int


class SeasonCreate(SeasonBase):
    pass

class SeasonResponse(BaseModel):
    seasonId: int
    year: int
    class Config:
        from_attributes = True

class Season(SeasonBase):
    seasonId: int
    races: List["Race"] = []

    class Config:
        from_attributes = True


class SprintResultBase(BaseModel):
    raceId: int
    driverId: int
    constructorId: int
    number: Optional[int]
    grid: Optional[int]
    position: Optional[int]
    positionText: Optional[str]
    positionOrder: Optional[int]
    points: Optional[int]
    laps: Optional[int]
    time: Optional[str]
    milliseconds: Optional[int]
    fastestLap: Optional[int]
    fastestLapTime: Optional[str]
    statusId: Optional[int]


class SprintResultCreate(SprintResultBase):
    pass

class SprintResultResponse(BaseModel):
    sprintResultId: int
    raceId: int
    driverId: int
    constructorId: int
    number: Optional[int]
    grid: Optional[int]
    position: Optional[int]
    positionText: Optional[str]
    positionOrder: Optional[int]
    points: Optional[int]
    laps: Optional[int]
    time: Optional[str]
    milliseconds: Optional[int]
    fastestLap: Optional[int]
    fastestLapTime: Optional[str]
    statusId: Optional[int]

    class Config:
        from_attributes = True

class SprintResult(SprintResultBase):
    sprintResultId: int
    race: "Race"
    constructor: "Constructor"
    driver: "Driver"
    status: "Status"

    class Config:
        from_attributes = True


class StatusBase(BaseModel):
    status: str


class StatusCreate(StatusBase):
    pass

class StatusResponse(BaseModel):
    statusId: int
    year: int

    class Config:
        from_attributes = True

class Status(StatusBase, IDBase):
    results: List["Result"] = []
    sprint_results: List["SprintResult"] = []
    class Config:
        from_attributes = True
