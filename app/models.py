from enum import Enum
from pydantic import BaseModel


class TransactionType(str, Enum):
    CREDIT="credit"
    DEBIT= "debit"
    

class TransactionCreate(BaseModel):
    user_id: str
    amount: int
    type: TransactionType
