######################### DAY 2 ############################
transactions = [
  {"user_id":"u1","amount":100,"type":"credit"},
  {"user_id":"u1","amount":40,"type":"debit"},
  {"user_id":"u2","amount":999,"type":"credit"},
  {"user_id":"u1","amount":-5,"type":"credit"},      # ignore
  {"user_id":"u1","type":"credit"},                  # ignore
  {"user_id":"u1","amount":"10","type":"credit"},    # ignore
  {"user_id":"u1","amount":7,"type":"refund"}        # ignore
]

def compute_balance(transactions, user_id):
    balance = 0

    for transaction in transactions:
        #amount = transaction[0]["amount"]   # ❌ wrong
        #card_type = transaction[0]["type"]  # ❌ wrong
        amount = transaction.get("amount")
        card_type = transaction.get("type")
        """Why .get()? Because if the key is missing, it returns None instead of crashing. That helps with validation."""
        # validation checks go here

        if transaction.get("user_id") != user_id:
            continue

        """
        if not isinstance(amount, int):
        That already covers:
        None
        string
        float
        anything not int
        So you do not need amount is None separately.

        """
        if not isinstance(amount, int):
            continue
        
        """
        1.If amount is None → continue
        2.If not int → continue
        3.If amount < 0 → continue
        4.If type not in ("credit", "debit") → continue
        
        """
        # if amount < 0 and amount is None: ❌ wrong if amount is None, the comparison amount < 0 will already crash.
        if amount < 0:
            continue
        # Remove the unnecessary if amount >= 0:  already filtered amount < 0 above.
        if card_type != "credit" and card_type != "debit":
            continue
        if card_type == "credit":
            balance+=amount 

        elif card_type == "debit":
            balance-=amount
    print(balance)
    return  balance

################## DAY 3 ###############################
transactions = [
  {"user_id": "u1", "amount": 100, "type": "credit"},
  {"user_id": "u1", "amount": 50, "type": "debit"},
  {"user_id": "u1", "amount": 70, "type": "credit"},
  {"user_id": "u2", "amount": 999, "type": "credit"},
]

"""
It should return True if:

The user has 3 or more transactions

And at least 2 of them are debits

And the total debit amount > 100

Otherwise return False.
"""

def has_suspicious_activity(transactions, user_id):
    tx_count =  0
    debit_count = 0
    debit_sum = 0
    for tx in transactions:
        # skip other users
        if tx.get("user_id") != user_id:
            continue
        tx_count+=1
        # check debit
        if tx.get("type") == "debit":
            debit_count+=1
            debit_sum += tx.get("amount",0)

    return tx_count>= 3 and debit_count>=2 and debit_sum > 100
    
has_suspicious_activity(transactions, "u1")

###################### DAY 4 #################

from fastapi import FastAPI
from sqlalchemy import text, create_engine
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL","")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def db_init():
    query = text("""
                 CREATE TABLE IF NOT EXISTS transactions
                 (id SERIAL PRIMARY KEY,
                 user_id TEXT NOT NULL,
                 amount INT NOT NULL,
                 type TEXT NOT NULL)
                 """);
    with engine.begin() as conn:
        conn.execute(query)

db_init()
# (psycopg2.errors.SyntaxError) syntax error at or near "id" had this error cause I didn't put attribut in ()

"""
We use SUM to aggregate all transaction contributions into a single balance value.
We use a CASE expression to conditionally treat credits as positive amounts and debits as negative amounts.
We restrict the rows with WHERE user_id = :user_id so the aggregation applies only to the specified user.
Since SUM returns NULL when there are no matching rows, we wrap it with COALESCE(..., 0) to default the balance to zero.
"""
@app.get("/users/{user_id}/balance")
def get_balance(user_id: str):
    query = text("""
                SELECT COALESCE(SUM(
                    CASE
                        WHEN type = 'credit' THEN amount
                        WHEN type = 'debit' THEN -amount
                        ELSE 0  
                    END  
                 ),0
                 ) AS balance
                FROM transactions
                WHERE user_id :user_id
                 """)
    with engine.cursor() as conn:
        result = conn.execute(query,{"user_id":user_id})
        row = result.mappings().one()
        balance = {"user_id":user_id, "balance": row["balance"]}
    return balance