import json


class CreatePayment:
    def __init__(self):
        self.purchase = 123
        self.amount = 10.0
        self.currency = 'EUR'

    def from_json(self, value):
        parsed = json.loads(value)
        self.purchase = parsed['purchase']
        self.amount = parsed['amount']
        self.currency = parsed['currency']
        return self

    def valid_payment(self):
        return json.dumps(self.__dict__)

    def custom_payment(self, purchase, amount, currency):
        self.purchase = purchase
        self.amount = amount
        self.currency = currency
        return json.dumps(self.__dict__)


# class can be removed after API is fixed and returns list of objects
class GetPayment:
    def __init__(self):
        self.payment_id = None
        self.purchase = None
        self.name = None
        self.amount = None
        self.currency = None
        self.processed = None

    def from_list(self, values_list):
        if len(values_list) != 6:
            raise Exception(f"Values list must contain exactly 6 elements")

        self.payment_id = values_list[0]
        self.purchase = values_list[1]
        self.name = values_list[2]
        self.amount = values_list[3]
        self.currency = values_list[4]
        self.processed = values_list[5]
        return self

    def convert_from_request(self, create_payment, user, payment_id, processed=0):
        if not isinstance(create_payment, CreatePayment):
            raise Exception("Please, provide valid CreatePayment instance")

        self.payment_id = payment_id  # cannot predict auto-generated value
        self.name = user
        self.purchase = create_payment.purchase
        self.amount = create_payment.amount
        self.currency = create_payment.currency
        self.processed = processed
        return self

    def to_json(self):
        return json.dumps(self.__dict__)


def get_payments_from_list(payments_list):
    return [GetPayment().from_list(payment) for payment in payments_list]
