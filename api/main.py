from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = crud.get_transaction(db, tx_hash=transaction.tx_hash)
    if db_transaction:
        raise HTTPException(status_code=400, detail="Transaction already exists")
    return crud.create_transaction(db=db, transaction=transaction)

@app.get("/transactions/", response_model=list[schemas.Transaction])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions_result = crud.get_transactions(db, skip=skip, limit=limit)
    print(f"Retrieved {len(transactions_result)} transactions from the database.")
    return transactions_result

@app.get("/transactions/{tx_hash}", response_model=schemas.Transaction)
def read_transaction(tx_hash: str, db: Session = Depends(get_db)):
    transaction = crud.get_transaction(db, tx_hash=tx_hash)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction