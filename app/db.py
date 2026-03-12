from sqlalchemy import text, create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL", DATABASE_URL)

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set yet!!")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


