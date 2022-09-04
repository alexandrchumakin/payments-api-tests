# REST API test automation
Current version of tests are done to show all the fixes in the initial app deployed to [this url](https://alexandrchumakin-finance-app.builtwithdark.com)

## Local setup
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
