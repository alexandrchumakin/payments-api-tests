import pytest
from delayed_assert import delayed_assert

from clients.api import ApiClient
from model.payments import CreatePayment

api = ApiClient()
payment = CreatePayment()


@pytest.mark.parametrize(('purchase', 'amount', 'currency'), [
    (123, 10.10, "EUR"),
    (124, 11.12, "USD"),
    (125, 122.0, "TRY"),
])
def test_create_valid_payment(purchase, amount, currency):
    body = payment.custom_payment(purchase=purchase, amount=amount, currency=currency)
    response = api.create_payment(body)
    delayed_assert.expect(response.body['paymentId'] is not None, 'paymentId is empty')
    delayed_assert.expect(response.status == 201, f"Invalid status code {response.status}")
    delayed_assert.assert_expectations()
    api.delete_payment(response.body['paymentId'])


def test_duplicate_payment():
    body = payment.valid_payment()
    response1 = api.create_payment(body)
    response2 = api.create_payment(body)
    assert response2.status == 400
    api.delete_payment(response1.body['paymentId'])


@pytest.mark.parametrize(('test_name', 'purchase', 'amount', 'currency'), [
    ('empty currency', 126, 12.20, ""),
    ('non-existent currency', 128, 0, "ABC"),
    ('currency with invalid length', 128, 0, "US"),
    ('currency in lower case', 128, 0, "usd"),
    ('currency ends with invalid symbol', 128, 0, "USDa"),
    ('currency in unsupported encoding', 128, 0, "РУБ"),
    ('negative amount', 130, -22.12, "EUR"),
])
def test_create_invalid_payment(test_name, purchase, amount, currency):
    body = payment.custom_payment(purchase=purchase, amount=amount, currency=currency)
    response = api.create_payment(body)
    assert response.status == 400


@pytest.mark.parametrize(('test_name', 'purchase', 'amount', 'currency'), [
    ('empty amount', 129, '', "EUR"),
    ('purchase is decimal', 12.12, 33, "EUR"),
    ('purchase is empty string', '', 33, "EUR"),
    ('zero amount', 131, 0, "EUR"),
    ('negative zero amount', 132, -0, "EUR"),
    ('negative purchase', -1, 33, "EUR"),
    ('invalid purchase type', [], 33.22, "EUR"),
    ('invalid amount type', 130, ['test'], "EUR"),
    ('invalid currency type', 130, 54.4, False),
])
def test_create_invalid_types_payment(test_name, purchase, amount, currency):
    body = payment.custom_payment(purchase=purchase, amount=amount, currency=currency)
    response = api.create_payment(body)
    assert response.status == 500
