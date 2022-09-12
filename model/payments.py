import json
import random


class CreatePayment:
    def __init__(self):
        self.purchase = None
        self.amount = None
        self.currency = None

    def valid_payment(self):
        self.purchase = random.randrange(100, 1000)
        self.amount = 10.0
        self.currency = 'EUR'
        return json.dumps(self.__dict__)

    def custom_payment(self, purchase, amount, currency):
        self.purchase = purchase
        self.amount = amount
        self.currency = currency
        return json.dumps(self.__dict__)
