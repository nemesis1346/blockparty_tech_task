python -m venv venv
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install fastapi uvicorn pytest httpx
pip freeze > requirements.txt