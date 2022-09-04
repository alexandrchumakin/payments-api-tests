# REST API test automation
There are two types of tests: 
- [Pytest](pytests) with test automation framework in Python and some libraries like requests and delayed-assert
- [RobotFramework-based tests](robot_tests) without any custom Python code

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

### Test results
You can access test results without local tests execution 
- [Robot framework test results](robot_results)
- [Pytest results](pytest_result) 

### Current status of target application under testing

#### Bugs
- API call without auth should return 401, not 403
- Payments can be processed with non-admin user
- Missing currency type validation
- Missing currency length and case validation
- Internal Server Error on payment creation with invalid `purchase` or `amount` field 

#### Business improvements
- We should have 201 status code on successful payment creation, not 200
- Create payment response should return paymentId, not `{"created": 1}` 
- Get payments endpoint should return a list of dictionaries (e.g. `[{"paymentId": 1, "amount": 123.45...}]`), not a list of lists
- User password should be restricted to be so weak
- Username and password should not be allowed to be the same 
- Do not allow to create a payment with missing currency in the system 
- Add "unprocessed" field to process payments endpoint to identify how many payments haven't been processed 
- Do not allow to create a duplicate payments
- Add more secured authentication method like OAuth2 
- Fix delete endpoint response to only return empty body with 204 status code if payment is deleted, 404 if not found and 400 if something went wrong 

#### Technical improvements
- requirements.txt with dependencies and clear instruction with how to use it in readme
- dockerfile to build an image with app and documentation how to run container and access it
- currencies list should be expanded either via library or some public API
- each API call takes around 2 seconds that is unacceptably slow, database migration should fix this problem

#### What should be tested if SQLite is migrated to MySQL/Oracle/MSSQL
- we can use CI machines with less RAM as SQLite requires a lot of memory with growing data in it
- we'll need to retest all the data types after migration (e.g. Float is 8 bytes in SQLite, but 4 bytes in MySQL)
- I would run performance test before and after migration to see how faster service became
- check of creating the same objects as syntax for existing and non-existing object is different
 