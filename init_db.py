from api.database import SessionLocal, engine
from api import models, schemas, crud
from api.mock_data import MOCK_TRANSACTIONS

models.Base.metadata.create_all(bind=engine)


db = SessionLocal()
for tx in MOCK_TRANSACTIONS:
    crud.create_transaction(db, schemas.TransactionCreate(**tx))
db.close()