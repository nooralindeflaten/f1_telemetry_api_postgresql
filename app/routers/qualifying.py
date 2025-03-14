# controllers.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, get_db
from app.crud import (
    create_qualifying,
    update_qualifying_position,
    delete_qualifying,
    get_qualifying_id)
from app import schemas
from typing import List

router = APIRouter()


@router.post("/qualifying", response_model=schemas.QualifyingResponse)
def add_qualifying(qualifying: schemas.QualifyingResponse, db: Session = Depends(get_db)):
    return create_qualifying(db, qualifying)



@router.get("/qualifying/{qualify_id}", response_model=List[schemas.QualifyingResponse])
def get_qualifying(qualify_id: int, db: Session = Depends(get_db)):
    return get_qualifying_id(db, qualify_id)


@router.put("/qualifying/{qualifying_id}", response_model=schemas.QualifyingResponse)
def update_position(qualifying_id: int, new_position: int, db: Session = Depends(get_db)):
    return update_qualifying_position(db, qualifying_id, new_position)

@router.delete("/qualifying/{qualifying_id}")
def delete_qualifying(qualifying_id: int, db: Session = Depends(get_db)):
    return delete_qualifying(db, qualifying_id)

