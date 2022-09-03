# REST API test automation
There are two types of tests: 
- Pytest with test automation framework in Python and some libraries like requests and delayed-assert
- RobotFramework-based tests without any custom Python code

## Local setup
- In order to run tests locally, you need to run dummy finance app that cannot be shared here.
- Python 3.8+
- [pip](https://pypi.org/project/pip/)  
- Install project dependencies. To do that with pip and virtualenv:
  - pip install virtualenv
  - virtualenv -p python3 .venv
  - virtualenv .venv
  - source .venv/bin/activate
  - pip install -r requirements.txt 

## Run test
Without any additional output: `pytest pytests/`

With all logs: `pytest -s pytests/`

With htlm-report generation: `pytest --html=report.html --self-contained-html pytests/`
