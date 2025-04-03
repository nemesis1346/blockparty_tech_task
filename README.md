# Blockparty Tech Assessment


## Setup:

# 1. Create and activate virtual environment (Mac/Linux)
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install fastapi uvicorn pytest httpx

# 3. Generate requirements.txt
pip freeze > requirements.txt


#Running the project:
uvicorn api.main:app --reload

the app should be running in http://127.0.0.1:8000/docs