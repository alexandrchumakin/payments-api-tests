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
 - locally with pre-setup above: `python main.py` (it will produce report.html in a root of this project)
 - in CI via GitHub Actions. Latest test report can be found [here](https://alexandrchumakin.github.io/payments-api-tests/)
