# generate_openapi.py
from fastapi import FastAPI
from api.main import app  # Import your FastAPI app
import json

if __name__ == "__main__":
    openapi_schema = app.openapi()
    with open("openapi.json", "w") as f:
        json.dump(openapi_schema, f)