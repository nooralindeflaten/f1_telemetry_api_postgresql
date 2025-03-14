# controllers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal, get_db
from typing import List

router = APIRouter()

# Route to get all constructor standings
@router.get("/constructor_standings", response_model=List[schemas.ConstructorStandingResponse])
def get_constructor_standings(db: Session = Depends(get_db)):
    return crud.get_constructor_standings(db)

# Route to get a constructor standing by ID
@router.get("/constructor_standings/{standing_id}", response_model=schemas.ConstructorStandingResponse)
def get_constructor_standing(standing_id: int, db: Session = Depends(get_db)):
    db_constructor_standing = crud.get_constructor_standing_by_id(db, standing_id)
    if db_constructor_standing is None:
        raise HTTPException(status_code=404, detail="Constructor standing not found")
    return db_constructor_standing

# Route to create a new constructor standing
@router.post("/constructor_standings", response_model=schemas.ConstructorStandingResponse)
def create_constructor_standing(constructor_standing: schemas.ConstructorStandingCreate, db: Session = Depends(get_db)):
    return crud.create_constructor_standing(db, constructor_standing)
