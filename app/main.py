from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from app.models import TransactionCreate, TransactionType

load_dotenv()

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL", "")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def init_db():
    create_sql = text("""
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        user_id TEXT NOT NULL,
        amount INT NOT NULL,
        type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)
    with engine.begin() as conn:
        conn.execute(create_sql)

@app.get("/health")
def health():
    # proves app boots
    return {"status": "ok"}

@app.get("/db-check")
def db_check():
    # proves DB connectivity
    with engine.connect() as conn:
        
        val = conn.execute(text("select 1")).scalar_one()
    return {"db": "ok", "select_1": val}


@app.post("/transactions")
def TransctionCreate(payload: TransactionCreate):
    params = { "user_id":payload.user_id, "amount": payload.amount, 'type':payload.type.value}
    query = text("""
        INSERT INTO transactions (user_id, amount, type)
        VALUES (:user_id, :amount, :type)
        RETURNING id, user_id, amount, type, created_at;
    """)
    with engine.begin() as conn:
        result = conn.execute(query,params)
        row = result.mappings().one()
    return row