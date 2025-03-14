from sqlalchemy import Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from .database import Base

class Driver(Base):
    __tablename__ = 'drivers'
    driverId = Column(Integer, primary_key=True)
    driverRef = Column(String)
    number = Column(Integer)
    code = Column(String)
    forename = Column(String)
    surname = Column(String)
    dob = Column(Date)
    nationality = Column(String)

 # Relationships
    results = relationship('Result', back_populates='driver')
    pit_stops = relationship('PitStop', back_populates='driver')
    qualifying = relationship('Qualifying', back_populates='driver')
    lap_times = relationship('LapTime', back_populates='driver')
    driver_standings = relationship('DriverStanding', back_populates='driver')
    sprint_results = relationship('SprintResult', back_populates='driver')

class Status(Base):
    __tablename__ = 'status'
    statusId = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)

    # Relationships
    results = relationship('Result', back_populates='status')
    sprint_results = relationship('SprintResult', back_populates='status')


class Season(Base):
    __tablename__ = 'seasons'
    seasonId = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    # Relationship to races
    races = relationship('Race', back_populates='season')

class Constructor(Base):
    __tablename__ = 'constructors'
    constructorId = Column(Integer, primary_key=True)
    constructorRef = Column(String, nullable=False)
    name = Column(String, nullable=False)
    nationality = Column(String)

    #Relationships
    constructor_results = relationship('ConstructorResult', back_populates='constructor')
    constructor_standings = relationship('ConstructorStanding', back_populates='constructor')
    results = relationship('Result', back_populates='constructor')
    qualifying = relationship('Qualifying', back_populates='constructor')
    sprint_results = relationship('SprintResult', back_populates='constructor')



class Circuit(Base):
    __tablename__ = 'circuits'
    circuitId = Column(Integer, primary_key=True)
    circuitRef = Column(String)
    name = Column(String)
    location = Column(String)
    country = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    alt = Column(Integer)

    # Relationship to races
    races = relationship('Race', back_populates='circuit')



class Race(Base):
    __tablename__ = 'races'
    #raceId
    raceId = Column(Integer, primary_key=True)
    #seasonId
    seasonId = Column(Integer, ForeignKey('seasons.seasonId'))
    #round of current season
    round = Column(Integer)
    #circuitID
    circuitId = Column(Integer, ForeignKey('circuits.circuitId'))
    #name of circuit
    name = Column(String, nullable=False)
    #Date of race
    date = Column(Date)
    #time of race-start
    time = Column(Time)
    #Time and date for different events
    fp1_date = Column(Date)
    fp1_time = Column(Time)
    fp2_date = Column(Date)
    fp2_time = Column(Time)
    fp3_date = Column(Date)
    fp3_time = Column(Time)
    quali_date = Column(Date)
    quali_time = Column(Time)
    sprint_date = Column(Date)
    sprint_time = Column(Time)

    # Relationships
    season = relationship('Season', back_populates='races')
    circuit = relationship('Circuit', back_populates='races')
    results = relationship('Result', back_populates='race', cascade="all, delete-orphan")
    sprint_results = relationship('SprintResult', back_populates='race')
    qualifying = relationship('Qualifying', back_populates='race')
    pit_stops = relationship('PitStop', back_populates='race')
    lap_times = relationship('LapTime', back_populates='race')
    driver_standings = relationship('DriverStanding',back_populates='race')
    constructor_results = relationship('ConstructorResult', back_populates='race')
    constructor_standings = relationship('ConstructorStanding', back_populates='race')

class Result(Base):
    __tablename__ = 'results'
    resultId = Column(Integer, primary_key=True)
    raceId = Column(Integer, ForeignKey('races.raceId'))
    driverId = Column(Integer, ForeignKey('drivers.driverId'))
    constructorId = Column(Integer, ForeignKey('constructors.constructorId'))
    number = Column(Integer)
    grid = Column(Integer)
    position = Column(Integer)
    positionText = Column(String)
    positionOrder = Column(Integer)
    points = Column(Integer)
    laps = Column(Integer)
    time = Column(String)
    milliseconds = Column(Integer)
    fastestLap = Column(Integer)
    rank = Column(Integer)
    fastestLapTime = Column(String)
    fastestLapSpeed = Column(Float)
    statusId = Column(Integer, ForeignKey('status.statusId'))

    #Relationships
    race = relationship('Race', back_populates='results')
    driver = relationship('Driver', back_populates='results')
    constructor = relationship('Constructor', back_populates='results')
    status = relationship('Status', back_populates='results')

class PitStop(Base):
    __tablename__ = 'pit_stops'
    pitStopId = Column(Integer, primary_key=True, autoincrement=True)
    raceId = Column(Integer, ForeignKey('races.raceId'))
    driverId = Column(Integer, ForeignKey('drivers.driverId'))
    lapId = Column(Integer, ForeignKey('lap_times.lapId'))
    stop = Column(Integer)
    lap = Column(Integer)
    time = Column(Time)
    duration = Column(String)
    milliseconds = Column(Integer)

    # Relationships
    race = relationship('Race', back_populates='pit_stops')
    driver = relationship('Driver', back_populates='pit_stops')
    lap_time = relationship("LapTime", back_populates="pit_stop", uselist=False)

class Qualifying(Base):
    __tablename__ = 'qualifying'
    qualifyId = Column(Integer, primary_key=True)
    raceId = Column(Integer, ForeignKey('races.raceId'))
    driverId = Column(Integer, ForeignKey('drivers.driverId'))
    constructorId = Column(Integer, ForeignKey('constructors.constructorId'))
    number = Column(Integer)
    position = Column(Integer)
    q1 = Column(String)
    q2 = Column(String)
    q3 = Column(String)

    # Relationships
    race = relationship('Race', back_populates='qualifying')
    driver = relationship('Driver', back_populates='qualifying')
    constructor = relationship('Constructor', back_populates='qualifying')

class ConstructorResult(Base):
    __tablename__ = 'constructor_results'
    constructorResultsId = Column(Integer, primary_key=True)
    raceId = Column(Integer, ForeignKey('races.raceId'))
    constructorId = Column(Integer, ForeignKey('constructors.constructorId'))
    points = Column(Integer)
    status = Column(String, nullable=True)

    #relationships
    race = relationship('Race', back_populates='constructor_results')
    constructor = relationship('Constructor', back_populates='constructor_results')


class ConstructorStanding(Base):
    __tablename__ = 'constructor_standings'
    constructorStandingsId = Column(Integer, primary_key=True)
    raceId = Column(Integer, ForeignKey('races.raceId'))
    constructorId = Column(Integer, ForeignKey('constructors.constructorId'))
    points = Column(Integer)
    position = Column(Integer)
    positionText = Column(String)
    wins = Column(Integer)

    #relationships
    race = relationship('Race', back_populates='constructor_standings')
    constructor = relationship('Constructor', back_populates='constructor_standings')



class DriverStanding(Base):
    __tablename__ = 'driver_standings'
    driverStandingsId = Column(Integer, primary_key=True)
    raceId = Column(Integer, ForeignKey('races.raceId'))
    driverId = Column(Integer, ForeignKey('drivers.driverId'))
    points = Column(Integer)
    position = Column(Integer)
    positionText = Column(String)
    wins = Column(Integer)

    #Relationships
    race = relationship('Race', back_populates='driver_standings')
    driver = relationship('Driver', back_populates='driver_standings')

class LapTime(Base):
    __tablename__ = 'lap_times'
    lapId = Column(Integer, primary_key=True, autoincrement=True)
    raceId = Column(Integer, ForeignKey('races.raceId'))
    driverId = Column(Integer, ForeignKey('drivers.driverId'))
    lap = Column(Integer)
    position = Column(Integer)
    time = Column(String)
    milliseconds = Column(Integer)

    # Relationships
    race = relationship('Race', back_populates='lap_times')
    driver = relationship('Driver', back_populates='lap_times')
    pit_stop = relationship("PitStop", back_populates="lap_time", uselist=False)

class SprintResult(Base):
    __tablename__ = 'sprint_results'
    sprintResultId = Column(Integer, primary_key=True)
    raceId = Column(Integer, ForeignKey('races.raceId'))
    driverId = Column(Integer, ForeignKey('drivers.driverId'))
    constructorId = Column(Integer, ForeignKey('constructors.constructorId'))
    number = Column(Integer)
    grid = Column(Integer)
    position = Column(Integer)
    positionText = Column(String)
    positionOrder = Column(Integer)
    points = Column(Integer)
    laps = Column(Integer)
    time = Column(String)
    milliseconds = Column(Integer)
    fastestLap = Column(Integer)
    fastestLapTime = Column(String)
    statusId = Column(Integer, ForeignKey('status.statusId'))

    #Relationships
    race = relationship('Race', back_populates='sprint_results')
    driver = relationship('Driver', back_populates='sprint_results')
    constructor = relationship('Constructor', back_populates='sprint_results')
    status = relationship('Status', back_populates='sprint_results')


