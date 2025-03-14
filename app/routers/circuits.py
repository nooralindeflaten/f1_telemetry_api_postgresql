from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Circuit, CircuitBase, CircuitCreate, CircuitUpdate, RaceResponse
from app import crud, models
from typing import List

router = APIRouter()

@router.get("/circuits/")
def get_all_circuits(db: Session = Depends(get_db)):
    return crud.get_circuits(db=db)

@router.get("/circuits/{circuitId}", response_model=Circuit)
def get_circuit(circuit_id: int, db: Session = Depends(get_db)):
    circuit = crud.get_circuit(db, circuit_id)
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return circuit

@router.get("/circuits/{circuitId}/races/", response_model=List[RaceResponse])
def get_circuit_race(circuit_id: int, db: Session = Depends(get_db)):
    races = crud.get_races_on_circuit(db, circuit_id=circuit_id)
    if not races:
        raise HTTPException(status_code=404, detail="Races not found")

@router.post("/circuits/", response_model=Circuit)
def create_Circuit(Circuit: CircuitCreate, db: Session = Depends(get_db)):
    return crud.create_circuit(db, Circuit)

@router.put("/circuits/{circuit_id}", response_model=Circuit)
def update_Circuit(Circuit_id: int, Circuit_update: CircuitUpdate, db: Session = Depends(get_db)):
    updated_Circuit = crud.update_circuit(db, Circuit_id, Circuit_update)
    if not updated_Circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return updated_Circuit

@router.delete("/{circuit_id}")
def delete_Circuit(Circuit_id: int, db: Session = Depends(get_db)):
    deleted_Circuit = crud.delete_circuit(db, Circuit_id)
    if not deleted_Circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return {"message": "Circuit deleted"}
