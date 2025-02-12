
## About The Project

This project covers API and UI automation for different applications.
It is written on Python and Behave, UI check uses Selenium for Web
API part covers by Python requests

Before the run, please make sure Fin Excange app is running on port 8080
## Get Started with Docker:
Make sure you have Docker running on your machine
#### Build the project via docker:
    docker build -t tonygod/behave-tests:latest https://github.com/inTonyGodWeTrust/behave-python-api-ui.git#main
#### Run the project via docker:
    docker run --rm -e API_BASE_URL="http://host.docker.internal:8080" tonygod/behave-tests:latest
## Get Started locally:
Make sure you have installed python 3 on your machine

#### 1. Clone repopository by the git command to specific place:
    git clone https://github.com/inTonyGodWeTrust/behave-python-api-ui.git
#### 2. Go to the project folder:
    cd behave-python-api-ui
#### 3. Creating a Virtual Environment:
    python3 -m venv venv
#### 4. Activating the Virtual Environment (for Mac/ Linux):
    source venv/bin/activate
#### 4. Installing Dependencies:
    pip install --no-cache-dir -r requirements.txt
#### 4. Running Tests with behave (run all tests in 1 execution):
    behave    
