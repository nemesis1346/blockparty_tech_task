import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from api import models, schemas
from api.main import create_transaction, read_transactions, read_transaction
from api.schemas import TransactionCreate

# Test data
TEST_TRANSACTION = {
    "tx_hash": "0x1e8a2a258283c7",
    "from_address": "0xfromaddress123",
    "to_address": "0xtoaddress456",
    "amount": 1.5
}

def test_create_transaction(db_session: Session):
    """Test transaction creation and duplicate prevention"""
    # Clean slate
    db_session.query(models.Transaction).delete()
    db_session.commit()
    
    # Test successful creation
    transaction_data = TransactionCreate(**TEST_TRANSACTION)
    result = create_transaction(transaction_data, db_session)
    assert result.tx_hash == TEST_TRANSACTION["tx_hash"]
    assert result.from_address == TEST_TRANSACTION["from_address"]
    assert result.amount == TEST_TRANSACTION["amount"]
    
    # Test duplicate prevention
    with pytest.raises(HTTPException) as exc_info:
        create_transaction(transaction_data, db_session)
    assert exc_info.value.status_code == 400
    assert "already exists" in exc_info.value.detail

def test_get_all_transactions(db_session: Session):
    """Test retrieving all transactions with pagination"""
    # Clean slate
    db_session.query(models.Transaction).delete()
    db_session.commit()
    
    # Create test data
    transaction_data = TransactionCreate(**TEST_TRANSACTION)
    create_transaction(transaction_data, db_session)
    
    # Test basic retrieval
    result = read_transactions(skip=0, limit=100, db=db_session)
    assert len(result) == 1
    assert isinstance(result, list)
    assert result[0].tx_hash == TEST_TRANSACTION["tx_hash"]

def test_get_valid_transaction(db_session: Session):
    """Test retrieving a specific transaction"""
    # Clean slate
    db_session.query(models.Transaction).delete()
    db_session.commit()
    
    # Create test data
    transaction_data = TransactionCreate(**TEST_TRANSACTION)
    create_transaction(transaction_data, db_session)
    
    # Test successful retrieval
    result = read_transaction(tx_hash=TEST_TRANSACTION["tx_hash"], db=db_session)
    assert result.tx_hash == TEST_TRANSACTION["tx_hash"]
    assert result.to_address == TEST_TRANSACTION["to_address"]

def test_get_nonexistent_transaction(db_session: Session):
    """Test handling of non-existent transactions"""
    # Clean slate (should be empty)
    db_session.query(models.Transaction).delete()
    db_session.commit()
    
    # Test error handling
    with pytest.raises(HTTPException) as exc_info:
        read_transaction(tx_hash="0x00000000000000", db=db_session)
    assert exc_info.value.status_code == 404
    assert "not found" in exc_info.value.detail

def test_pagination(db_session: Session):
    """Test pagination functionality"""
    # Clean slate
    db_session.query(models.Transaction).delete()
    db_session.commit()
    
    # Create multiple test transactions
    test_transactions = []
    for i in range(5):
        tx_data = TEST_TRANSACTION.copy()
        tx_data["tx_hash"] = f"0xtesthash{i}"
        transaction = TransactionCreate(**tx_data)
        create_transaction(transaction, db_session)
        test_transactions.append(tx_data["tx_hash"])
    
    # Test pagination
    result = read_transactions(skip=0, limit=2, db=db_session)
    assert len(result) == 2
    assert result[0].tx_hash in test_transactions
    
    result = read_transactions(skip=2, limit=2, db=db_session)
    assert len(result) == 2
    
    result = read_transactions(skip=4, limit=2, db=db_session)
    assert len(result) == 1
    
    # Test edge case
    result = read_transactions(skip=5, limit=2, db=db_session)
    assert len(result) == 0