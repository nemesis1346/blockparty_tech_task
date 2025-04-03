from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_transactions():
    response = client.get("/transactions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_valid_transaction():
    test_hash = "0x1e8a2a258283c7"
    response = client.get(f"/transactions/{test_hash}")
    assert response.status_code == 200
    assert response.json()["tx_hash"] == test_hash

def test_get_invalid_transaction():
    response = client.get("/transactions/invalid_hash")
    assert response.status_code == 422
    assert "must start with 0x" in response.json()["error"]

def test_get_nonexistent_transaction():
    response = client.get("/transactions/0x00000000000000")
    assert response.status_code == 404
    assert "not found" in response.json()["error"]