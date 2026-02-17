# ledger API - FastAPI + PostSQL

## Description
A backend REST API for managing financial transactions and computing user balances using SQL aggregation.
Built with FastAPI and PostgreSQL. Includes pagination, filtering, and database migrations.

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic 
- Docker
- Pytest

## How to Run
### 1. Impliment PostgreSQL on Docker

`docker run -d --name ledger-postgres \ 
-e POSTGRES_USER=ledger \ 
-e POSTGRES_PASSWORD=ledgerpass \ 
-e POSTGRES_DB=ledgerdb \ 
-p 5432:5432 \ 
postgres:16`

### 2. Install depenndecices

`pip install -r requirements.txt`

### 3. Run app with this command

`uvicorn main:app --reload`

## Example Endpoints
`POST /transactions`

`GET /users/{user_id}/balance`

Balance is computed using SQL conditional aggregation with CASE + SUM + COALESCE to avoid null values.

`GET /transactions?limit=&offset=`