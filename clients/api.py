import requests
import urllib3
from requests.auth import HTTPBasicAuth

from clients import parse_response

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ApiClient:
    def __init__(self, user='john', password='john'):
        self.user = user
        self.auth = HTTPBasicAuth(user, password)
        self.headers = {'Content-type': 'application/json'}
        self.host = 'https://alexandrchumakin-finance-app.builtwithdark.com'
        self.base_path = '/finance/api/v1.0/payments'

    def create_payment(self, body):
        print(f"Creating payment with body {body}")
        path = f"{self.host}{self.base_path}"
        r = requests.put(path, data=body, headers=self.headers, verify=False, auth=self.auth)
        return parse_response(r)

    def process_payments(self):
        print("Processing payments")
        path = f"{self.host}{self.base_path}"
        r = requests.post(path, headers=self.headers, verify=False, auth=self.auth)
        return parse_response(r)

    def get_payments(self):
        print("Retrieving all payments")
        path = f"{self.host}{self.base_path}"
        r = requests.get(path, headers=self.headers, verify=False, auth=self.auth)
        return parse_response(r)

    def delete_payment(self, payment_id):
        print(f"Deleting payment {payment_id}")
        path = f"{self.host}{self.base_path}/{payment_id}"
        r = requests.delete(path, headers=self.headers, verify=False, auth=self.auth)
        return parse_response(r)
