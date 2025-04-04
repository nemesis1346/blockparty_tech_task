# Blockparty Tech Assessment

For this challenge I used FastAPI and sql alchemy to setup the environment. I used sql models to give a model schema of the transactions to deal with the logic. Additionally I added a CRUD layer to allocate the logic of the endpoints of the API. Also I used some HTTP modules in order to respond properly to the client. I also added an extra point of POST in order to create a new transaction and I added some parameters to the getTransaction list to make it more customizable to the user.

Moreover I decided to add Swagger UI for testing the API, so is more intuitive for the user, te same swagger UI will be running in the deployment instance in Heroku

## Setup:

#### 1. Create and activate virtual environment (Mac/Linux)
```
# python version: 3.9.6

python3 -m venv venv
source venv/bin/activate # to activate the venv folder
```
#### 2. Generate requirements.txt
```
pip install -r requirements.txt
```

## Running the Api:

For using the API in Swagger:

```
uvicorn api.main:app --reload

# the app should be running in http://127.0.0.1:8000/docs
```

### Unit testing

I managed to setup the sql engine to not affect the "production" data but rather use another instance of the database to run the tests.

```
pytest tests/test_api.py -v
```

## Challenges

- Dependencies: sql and fastapi dependencies were crashing at the beginning so I needed to find a balance that can work in the requirements.txt. Some of the libraries that were failing were pydantic and starlette

- K6 setup was difficult to do it in python because they are binaries built in go, rather I created a javascript file to interact with the running api. 

- Pytest was having some dependencies problems that didnt let me create a ClientTest objet to simulate the http call therefore I decided just to test the functionality of the endpoints

### Deployment

I decided to publish this app in a Heroku instance so you guys can test it right away if needed. The app is running in the following URL:

```
https://blockparty-b1a10d1e5277.herokuapp.com/docs#
```

This deployment has the latest changes that are in this repo, meaning that is reading and writing from the SQL database which already imported the mock_data given


## k6 performance test

Prerequisites: 
- The api needs to be running with the command previously mentioned
- Needs to run inside venv environment

I wrote a simple script of simulating a quantity of VS(virtual users) that run under 1 minute and verifying that the response has some data. At the end of the test it will give you the ones that failed and the ones that succeeded. To run it you will need to install k6 by running the installation script I added:

```
chmod +x install-k6.sh
./install-k6.sh

# after this installation you should have k6 installed and you can run:
k6 run loadtest.js
```

* The results of an example of 100 VS in 1 min was:
```
 TOTAL RESULTS 

    checks_total.......................: 28956   480.711445/s
    checks_succeeded...................: 100.00% 28956 out of 28956
    checks_failed......................: 0.00%   0 out of 28956

    ✓ status is 200
    ✓ has data

    HTTP
    http_req_duration.......................................................: avg=207.4ms  min=199µs    med=121.19ms max=703.36ms p(90)=463.78ms p(95)=488.48ms
      { expected_response:true }............................................: avg=207.4ms  min=199µs    med=121.19ms max=703.36ms p(90)=463.78ms p(95)=488.48ms
    http_req_failed.........................................................: 0.00%  0 out of 28956
    http_reqs...............................................................: 28956  480.711445/s

    EXECUTION
    iteration_duration......................................................: avg=415.25ms min=162.17ms med=416.67ms max=732.44ms p(90)=492.49ms p(95)=512.63ms
    iterations..............................................................: 14478  240.355722/s
    vus.....................................................................: 100    min=100        max=100
    vus_max.................................................................: 100    min=100        max=100

    NETWORK
    data_received...........................................................: 297 MB 4.9 MB/s
    data_sent...............................................................: 3.4 MB 57 kB/s
```
