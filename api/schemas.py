from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    tx_hash: str
    from_address: str
    to_address: str
    amount: float

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True