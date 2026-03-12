
from fastapi import FastAPI
from sqlalchemy import text
from app.db import engine
from app.api.routes import health
from app.api.routes import transactions
from app.api.routes import balance



app = FastAPI()

app.include_router(health.router)
app.include_router(transactions.router)
app.include_router(balance.router)

@app.get("/db-check")
def db_check():
    # proves DB connectivity
    with engine.connect() as conn:
        
        val = conn.execute(text("select 1")).scalar_one()
    return {"db": "ok", "select_1": val}




    
