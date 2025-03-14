from app.database import engine, Base  # Make sure this path is correct
from app.models import PitStop,Qualifying,Result,Constructor,ConstructorResult,ConstructorStanding, Driver, DriverStanding,Season,SprintResult, Circuit, Race, LapTime,Status  # Import all models to create tables

def init_db():
    # Creates all tables from models if they don't exist yet
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅ Database tables created successfully!")
