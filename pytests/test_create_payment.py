import math

import pytest
from delayed_assert import delayed_assert

from clients.api import ApiClient
from model.payments import CreatePayment

api = ApiClient()
payment = CreatePayment()
payment_ids = []


@pytest.fixture(autouse=True)
def cleanup():
    yield
    last_payment = api.get_payments().body[-1]
    api.delete_payment(last_payment.payment_id)


@pytest.mark.parametrize(('purchase', 'amount', 'currency'), [
    (123, 10, "EUR"),
    (124, 11.12, "USD"),
    (125, 122, "TYR"),
])
def test_create_valid_payment(purchase, amount, currency):
    body = payment.custom_payment(purchase=purchase, amount=amount, currency=currency)
    response = api.create_payment(body)
    delayed_assert.expect(response.body['created'] == 1,
                          'created value is invalid')  # should check valid paymentId in response after fix
    delayed_assert.expect(response.status == 200,
                          f"Invalid status code {response.status}")  # should be changed to 201 after fix
    delayed_assert.assert_expectations()


@pytest.mark.parametrize(('test_name', 'purchase', 'amount', 'currency'), [
    ('empty currency', 126, 12.20, ""),
    ('non-existent currency', 128, 0, "ABC"),
    ('currency with invalid length', 128, 0, "US"),
    ('currency in lower case', 128, 0, "usd"),
    ('currency ends with invalid symbol', 128, 0, "USDa"),
    ('currency in unsupported encoding', 128, 0, "РУБ"),
    ('empty amount', 129, '', "EUR"),
    ('negative amount', 130, -22.12, "EUR"),
    ('zero amount', 131, 0, "EUR"),
    ('negative zero amount', 132, -0, "EUR"),
    ('amount is Euler`s number', 133, math.e, "EUR"),
    ('too much decimal points in amount', 134, 22.1212312343542312, "EUR"),
    ('negative purchase', -1, 33, "EUR"),
    ('purchase is decimal', 12.12, 33, "EUR"),
    ('purchase is empty string', '', 33, "EUR"),
    ('invalid purchase type', [], 33.22, "EUR"),
    ('invalid amount type', 130, ['test'], "EUR"),
    ('invalid currency type', 130, 54.4, False),
])
def test_create_invalid_payment(test_name, purchase, amount, currency):
    body = payment.custom_payment(purchase=purchase, amount=amount, currency=currency)
    response = api.create_payment(body)
    assert response.status == 400


def test_duplicate_payment():
    body = payment.valid_payment()
    api.create_payment(body)
    response = api.create_payment(body)
    assert response.status == 400
