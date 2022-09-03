import pytest
from delayed_assert import delayed_assert

from clients.api import ApiClient
from model.payments import CreatePayment


api = ApiClient(user="admin", password="admin")
payment = CreatePayment()


@pytest.fixture(autouse=True)
def cleanup():
    yield
    last_payment = api.get_payments().body[-1]
    api.delete_payment(last_payment.payment_id)


def test_process_valid_payment():
    api.create_payment(payment.valid_payment())
    response = api.process_payments()
    delayed_assert.expect(response.body['processed'] >= 1,
                          f"Invalid processed payments number: {response.body['processed']}")
    delayed_assert.expect(response.status == 200, f"Invalid status code {response.status}")
    delayed_assert.assert_expectations()


def test_process_all_payments():
    api.create_payment(payment.valid_payment())
    api.create_payment(payment.custom_payment(198, 99.99, "USD"))
    response = api.process_payments()
    delayed_assert.expect(response.body['processed'] >= 2,
                          f"Invalid processed payments number: {response.body['processed']}")
    all_payment = api.get_payments().body
    delayed_assert.expect(all_payment[-1].processed == 1, "Last payment is not processed")
    delayed_assert.expect(all_payment[-2].processed == 1, "Penult payment is not processed")
    delayed_assert.assert_expectations()
    api.delete_payment(all_payment[-2].payment_id)  # hook will only delete last payment


@pytest.mark.parametrize(('test_name', 'currency', 'init_amount', 'converted_amount'), [
    ('same currency', 'EUR', 10.10, 10.10),
    ('existing conversion rate', 'USD', 22, 18.48),
    ('non-existing conversion rate', 'TYR', 100, 5.52),  # bug with missing conversion rates
])
def test_money_conversion(test_name, currency, init_amount, converted_amount):
    body = payment.custom_payment(purchase=123, amount=init_amount, currency=currency)
    api.create_payment(body)
    api.process_payments()
    last_payment = api.get_payments().body[-1]
    delayed_assert.expect(last_payment.currency == "EUR", f"Currency {last_payment.currency} is not converted to EUR")
    delayed_assert.expect(last_payment.processed == 1, "Payment is not processed")
    delayed_assert.expect(last_payment.amount == converted_amount,
                          f"Converted amount {converted_amount} is invalid, actual is {last_payment.amount}")
    delayed_assert.assert_expectations()


def test_skip_invalid_payments_processing():
    init_amount = 10.2
    currency = "pjgerkg"
    body = payment.custom_payment(purchase=123, amount=init_amount, currency=currency)
    api.create_payment(body)
    api.process_payments()
    last_payment = api.get_payments().body[-1]
    delayed_assert.expect(last_payment.amount == init_amount, "Amount is changed")
    delayed_assert.expect(last_payment.processed == 0, "Payment with invalid currency is processed")
    delayed_assert.expect(last_payment.currency == currency, "Invalid currency is changed")
    delayed_assert.assert_expectations()


def test_cannot_process_with_non_admin():  # fails on bug
    user_api = ApiClient(user="john", password="john")
    user_api.create_payment(payment.valid_payment())
    response = user_api.process_payments()
    assert response.status == 403
