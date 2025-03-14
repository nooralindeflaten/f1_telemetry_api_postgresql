from fastapi import FastAPI
from app.routers import drivers, races, circuits, results, laps, seasons, sprint_results, status, pit_stops, constructor_results, constructor_standings, constructors
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict this later to specific domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(drivers.router)
app.include_router(circuits.router)
app.include_router(results.router)
app.include_router(races.router)
app.include_router(laps.router)
app.include_router(seasons.router)
app.include_router(sprint_results.router)
app.include_router(status.router)
app.include_router(pit_stops.router)
app.include_router(constructor_results.router)
app.include_router(constructor_standings.router)
app.include_router(constructors.router)

