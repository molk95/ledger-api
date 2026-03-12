from fastapi import APIRouter
from sqlalchemy import text
from app.db import engine

#########################  DAY 1 ################################
router = APIRouter()

# Since SUM returns NULL when there are no matching rows, we wrap it in COALESCE to default the balance to 0.
@router.get("/users/{user_id}/balance")
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

