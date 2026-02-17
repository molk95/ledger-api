from sqlalchemy import text, create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL","")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

"""
def init_db():
    query = text(
                 CREATE TABLE IF NOT EXISTS transactions(
                    id SERIAL PRIMARY KEY,
                     USER_ID TEXT NOT NULL,
                    AMOUNT INT NOT NULL,
                    TYPE TEXT NOT NULL   
                 )
                
                 )
    with engine.begin() as conn:
        result = conn.execute(query)
    return result
init_db()
"""
