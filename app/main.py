
from fastapi import FastAPI
from sqlalchemy import text, create_engine
import os
from dotenv import load_dotenv
from app.models import TransactionCreate

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL","")

app = FastAPI()

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def init_db():
    query = text("""
                 CREATE TABLE IF NOT EXISTS transactions(
                    id SERIAL PRIMARY KEY,
                     USER_ID TEXT NOT NULL,
                    AMOUNT INT NOT NULL,
                    TYPE TEXT NOT NULL   
                 )
                
                 """)
    with engine.begin() as conn:
        result = conn.execute(query)
    return result
init_db()

#########################  DAY 1 ################################
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

###################### DAY 2 ####################################
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

##################### DAY 4 #########################
# Since SUM returns NULL when there are no matching rows, we wrap it in COALESCE to default the balance to 0.
@app.get("/users/{user_id}/balance")
def get_balance(user_id: str):
    query = text("""
            SELECT COALESCE(SUM(
            CASE
                WHEN type = 'credit' THEN amount
                WHEN type = 'debit' THEN -amount
                ELSE 0
            END
                ),
                0
                ) AS balance
                FROM transactions
                WHERE user_id = :user_id
    """)
    with engine.connect() as conn:
        result =  conn.execute(query, {"user_id" :user_id})
        row = result.mappings().one()
        balance = {"user_id":user_id, "balance": row["balance"]}
    return balance
    
