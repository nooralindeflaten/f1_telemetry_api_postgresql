# F1 Telemetry API 🏎️
## 📖 Description
- This project is built using postgreSQL inside docker
- Sqlalchemy for communicating
- Schemas for verifying data and orm model handling
- crud functions for sqlalchemy-based sql functions
- Frontend React + Vite
  
## The code structure of a PostgreSQL database based FastAPI
🚀 Features
  - Gets specific data from endpoints such as Race results, lap_times etc.
  - Communicates with the server using python "sqlalchemy" models.
  - Has various filtering methods.
  - (In progress) Uses datasets from the models to train machine-learning models.
  - Verifies input/output data using a schemas script to ensure authenticity.
  - Uses environment variables to provide security features.
  - Uses alembic before applying changes to create a better understanding of documentation.
## 🏗️ Project Structure (Initial)
- FastAPI endpoints (routers/) handle HTTP requests.
- CRUD functions (crud.py) interact with the database.
- Schemas (schemas.py) define how data is structured.
- Models (models.py) define the database tables.
- Database session (database.py) creates and manages connections.
- Alembic migrations update the database schema.
```bash

/f1_telemetry_api/
|--alembic/               #Alembic generated data
├── app/
│   ├── __init__.py
│   ├── main.py           # Entry point for FastAPI app
│   ├── database.py       # Database connection and session management
│   ├── models.py         # SQLAlchemy models (or your ORM of choice)
│   ├── schemas.py        # Pydantic schemas for request/response validation
│   ├── crud.py           # Functions for database operations
│   ├── config.py         # Configuration variables (loaded from env vars)
|   |--data_loader.py     # Load data from .csv files
│   └── routers/
│       ├── __init__.py
│       ├── drivers.py    # Endpoints related to drivers
│       ├── races.py      # Endpoints related to races
│       └── laps.py
|       ...          # Endpoints related to data
├── frontend/
│   ├── __init__.py
│   └── test_api.py       # front-end setup
├── Dockerfile            # Containerization (if deploying)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```
## 🛠️ Installation & Setup
 1. Virtual environment
 - The project was loaded and developed inside an Anaconda dev environment
 - Download all dependencies into virtual env.
 2. PostgreSQL
    1. The first step is to create a PostgreSQL
        - Docker-compose.yml file containing, PostgreSQL 15 which runs as a service
        - Statement to restart automatically
        - Persistent storage to ensure database is not lost
        - Exposed port 5432, so it can connect to the FastAPI app.
    2. Creating environmental values
       - In the .env file variables have been created to avoid hardcoding credentials
    3. Start PostgreSQL in docker
        - run:
            ```sh
            docker-compose up -d
            ```
        - To interact with PostgreSQL:
          ```sh
          docker exec -it f1_telemetry_db psql -U f1user -d f1_telemetry
          ```
          Test:
          ```SQL
          SELECT 'PostgreSQL is working!' AS test_message;
          ```
  3. Creating database.py
    - Loads credentials from .env
    - Creates a connection engine for PostgreSQL
    - Defines SessionLocal to handle database sessions
    - Sets up Base for SQLAlchemy models

4. Initialize data
   - Created models.py for defining table structure and relationships between Primary-Foreign keys
   - Used init_db.py to run the initial setup of the tables
5. Alembic setup
   - install alembic
     ```bash
     pip install alembic
     alembic init alembic
        ```
  
## 🛠️ Usage
- API Endpoints, routers
- Some examples

| Method        | Endpoint                                     | Description   |
| ------------- |:--------------------------------------------:| :------------:|
| GET           | "/drivers/{driver_id}/driver_standings"      |get's the driver_standings related to the current driver       |
| GET           | "/drivers/{driver_id}/results"               |get's the results belonging to the current driver              |


## 🔗 Deployment
- Planning on using the containerized version of the FastAPI app to deploy a functional public API
- Set up data to easily be able to use for ML

## 📜 License
The csv files were downloaded directly to my local directory from: https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020?select=races.csv
