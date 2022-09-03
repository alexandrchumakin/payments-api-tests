import json


class CreatePayment:
    def __init__(self):
        self.purchase = 123
        self.amount = 10
        self.currency = 'EUR'

    def valid_payment(self):
        return json.dumps(self.__dict__)

    def custom_payment(self, purchase, amount, currency):
        self.purchase = purchase
        self.amount = amount
        self.currency = currency
        return json.dumps(self.__dict__)


# class can be removed after API is fixed and returns list of objects
class GetPayment:
    def __init__(self, values_list):
        if len(values_list) != 6:
            raise Exception(f"Values list must contain exactly 6 elements")

        self.payment_id = values_list[0]
        self.purchase = values_list[1]
        self.name = values_list[2]
        self.amount = values_list[3]
        self.currency = values_list[4]
        self.processed = values_list[5]


def get_payments_from_list(payments_list):
    return [GetPayment(payment) for payment in payments_list]
