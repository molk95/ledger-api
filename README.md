# Ledger API — FastAPI + PostgreSQL

## Description
A backend REST API for managing financial transactions and computing user balances using SQL aggregation.
Built with FastAPI and PostgreSQL. Includes database migrations and basic automated tests.

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- Pytest

## How to Run

### 1) Run PostgreSQL with Docker
```bash
docker run -d --name ledger-postgres \
  -e POSTGRES_USER=ledger \
  -e POSTGRES_PASSWORD=ledgerpass \
  -e POSTGRES_DB=ledgerdb \
  -p 5432:5432 \
  postgres:16
```
Add a `.env`:
```bash
DATABASE_URL=postgresql+psycopg2://ledger:ledgerpass@localhost:5432/ledgerdb
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Run migrations
```bash
alembic upgrade head
```
### 4. Start the API
```bash
uvicorn main:app --reload
```
If your entry point is `app/main.py`, use: `uvicorn app.main:app --reload`

## Example Endpoints
`POST /transactions`

`GET /users/{user_id}/balance`

Balance is computed using SQL conditional aggregation with `CASE + SUM + COALESCE` to avoid null values.

## Running Tests

```bash
pytest -q
```