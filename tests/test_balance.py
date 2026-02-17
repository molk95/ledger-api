from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import text
from app.main import app
from app.db import engine

client = TestClient(app)

def test_balance_for_users():
    with engine.begin() as conn:
        # clean database
        conn.execute(text("DELETE FROM transactions"))
        # in sert data
        conn.execute(text("""INSERT INTO transactions (user_id, amount, type) 
                                VALUES
                                    ('u1',100,'credit'),
                                    ('u1',40,'debit'),
                                    ('u2',999,'credit');
                                    """))
    response = client.get("/users/u1/balance")
    assert response.status_code == 200
    assert response.json() == {
        "user_id":"u1",
        "balance": 60
    }
    