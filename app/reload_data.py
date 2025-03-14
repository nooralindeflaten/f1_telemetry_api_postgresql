import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Result, DriverStanding, ConstructorStanding, ConstructorResult

def reload_results(db: Session):
    """Reload results data from CSV and update database."""
    rows_edited = 0
    file_path = "/Users/nooralindeflaten/Downloads/f1_results/results.csv"

    try:
        # Load CSV
        results = pd.read_csv(file_path)

        # Convert data types safely
        results['points'] = pd.to_numeric(results['points'], errors='coerce').fillna(0).astype(int)
        results['fastestLapSpeed'] = pd.to_numeric(results['fastestLapSpeed'], errors='coerce')

        for _, row in results.iterrows():
            existing_result = db.query(Result).filter(Result.resultId == row['resultId']).first()

            if existing_result:
                # Update only if there's a difference
                if (existing_result.points != row['points'] or
                    existing_result.fastestLapSpeed != row['fastestLapSpeed']):

                    existing_result.points = row['points']
                    existing_result.fastestLapSpeed = row['fastestLapSpeed']
                    rows_edited += 1
            else:
                continue  # Skip if the result does not exist

        # Commit changes
        db.commit()
        print(f"✅ {rows_edited} rows updated successfully!")

    except Exception as e:
        print(f"❌ Error loading results data: {e}")
        db.rollback()  # Rollback to avoid partial updates


def reload_driver_standings(db: Session):
    rows_edited = 0
    file_path = "/Users/nooralindeflaten/Downloads/f1_results/driver_standings.csv"

    try:
        # Load CSV
        results = pd.read_csv(file_path)

        # Convert data types safely
        results['points'] = pd.to_numeric(results['points'], errors='coerce').fillna(0).astype(int)

        for _, row in results.iterrows():
            existing_result = db.query(DriverStanding).filter(DriverStanding.driverStandingsId == row['driverStandingsId']).first()

            if existing_result:
                # Update only if there's a difference
                if (existing_result.points != row['points']):

                    existing_result.points = row['points']
                    rows_edited += 1
            else:
                continue  # Skip if the result does not exist

        # Commit changes
        db.commit()
        print(f"✅ {rows_edited} rows updated successfully!")

    except Exception as e:
        print(f"❌ Error loading results data: {e}")
        db.rollback()  # Rollback to avoid partial updates

def reload_constructor_standings(db: Session):
    rows_edited = 0
    file_path = "/Users/nooralindeflaten/Downloads/f1_results/constructor_standings.csv"

    try:
        # Load CSV
        results = pd.read_csv(file_path)

        # Convert data types safely
        results['points'] = pd.to_numeric(results['points'], errors='coerce').fillna(0).astype(int)

        for _, row in results.iterrows():
            existing_result = db.query(ConstructorStanding).filter(ConstructorStanding.constructorStandingsId == row['constructorStandingsId']).first()

            if existing_result:
                # Update only if there's a difference
                if (existing_result.points != row['points']):

                    existing_result.points = row['points']
                    rows_edited += 1
            else:
                continue  # Skip if the result does not exist

        # Commit changes
        db.commit()
        print(f"✅ {rows_edited} rows updated successfully!")

    except Exception as e:
        print(f"❌ Error loading results data: {e}")
        db.rollback()  # Rollback to avoid partial updates


def reload_constructor_results(db: Session):
    rows_edited = 0
    file_path = "/Users/nooralindeflaten/Downloads/f1_results/constructor_results.csv"

    try:
        # Load CSV
        results = pd.read_csv(file_path)

        # Convert data types safely
        results['points'] = pd.to_numeric(results['points'], errors='coerce').fillna(0).astype(int)

        for _, row in results.iterrows():
            existing_result = db.query(ConstructorResult).filter(ConstructorResult.constructorResultsId == row['constructorResultsId']).first()

            if existing_result:
                # Update only if there's a difference
                if (existing_result.points != row['points']):

                    existing_result.points = row['points']
                    rows_edited += 1
            else:
                continue  # Skip if the result does not exist

        # Commit changes
        db.commit()
        print(f"✅ {rows_edited} rows updated successfully!")

    except Exception as e:
        print(f"❌ Error loading results data: {e}")
        db.rollback()  # Rollback to avoid partial updates
def main():
    """Database session management."""
    db = SessionLocal()
    try:
        reload_constructor_results(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
