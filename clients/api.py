import requests
from requests.auth import HTTPBasicAuth

from clients import parse_response
from model.payments import get_payments_from_list


class ApiClient:
    def __init__(self, user='john', password='john'):
        self.auth = HTTPBasicAuth(user, password)
        self.headers = {'Content-type': 'application/json'}
        self.host = 'http://localhost:5000'
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
        parsed_resp = parse_response(r)
        parsed_resp.body = get_payments_from_list(parsed_resp.body['payments'])
        return parsed_resp
