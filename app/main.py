
from fastapi import FastAPI
from sqlalchemy import text
from app.db import engine
from app.models.transactions import TransactionCreate



app = FastAPI()



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
    
