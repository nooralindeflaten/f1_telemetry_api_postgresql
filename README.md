F1 Telemetry API 🏎️

The code structure of a PostgreSQL database based FastAPI
🚀 Features
  - Gets specific data from endpoints such as Race results, lap_times etc.
  - Communicates with the server using python "sqlalchemy" models.
  - Has various filtering methods.
  - (In progress) Uses datasets from the models to train machine-learning models.
  - Verifies input/output data using a schemas script to ensure authenticity.
  - Uses environment variables to provide security features.
  - Uses alembic before applying changes to create a better understanding of documentation.

🛠️ Usage
API Endpoints
Method	Endpoint	Description
GET	/drivers	Get all drivers
GET	/drivers/{id}	Get a driver by ID
POST	/drivers	Add a new driver
