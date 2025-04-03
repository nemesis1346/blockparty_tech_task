from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from .mock_data import MOCK_TRANSACTIONS
from typing import List, Dict

app = FastAPI(
    title="Transaction Mock API",
    description="API for mock blockchain transactions",
    version="1.0.0",
    openapi_tags=[{
        "name": "Transactions",
        "description": "Endpoints for transaction data"
    }]
)

@app.get("/transactions", 
         response_model=List[Dict],
         tags=["Transactions"],
         summary="Get all transactions")
async def get_all_transactions():
    """Retrieve complete transaction history"""
    return MOCK_TRANSACTIONS

@app.get("/transactions/{tx_hash}",
         response_model=Dict,
         tags=["Transactions"],
         summary="Get transaction by hash",
         responses={
             404: {"description": "Transaction not found"},
             422: {"description": "Invalid hash format"}
         })
async def get_transaction(tx_hash: str):
    """Retrieve specific transaction by its hash
    
    - **tx_hash**: Transaction hash starting with 0x
    """
    if not tx_hash.startswith('0x'):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Transaction hash must start with 0x"
        )
    
    transaction = next(
        (tx for tx in MOCK_TRANSACTIONS if tx["tx_hash"] == tx_hash), 
        None
    )
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction {tx_hash} not found"
        )
    
    return transaction

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "success": False
        }
    )