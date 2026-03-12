
#########################  DAY 1 ################################
from fastapi import APIRouter
from app.models.transactions import TransactionCreate
from app.db import engine
from sqlalchemy import text


router = APIRouter()
@router.post("/transactions")
def create_trasactions(payload:TransactionCreate ):
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

