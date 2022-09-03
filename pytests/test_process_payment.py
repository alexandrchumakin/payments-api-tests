import pytest
from delayed_assert import delayed_assert

from pytests.test_create_payment import payment, api


def test_process_valid_payment():
    body = payment.valid_payment()
    api.create_payment(body)
    response = api.process_payments()
    delayed_assert.expect(response.body['processed'] >= 1,
                          f"Invalid processed payments number: {response.body['processed']}")
    delayed_assert.expect(response.status == 200, f"Invalid status code {response.status}")
    delayed_assert.assert_expectations()


@pytest.mark.parametrize(('test_name', 'currency', 'init_amount', 'converted_amount'), [
    ('same currency', 'EUR', 10.10, 10.10),
    ('existing conversion rate', 'USD', 22, 18.48),
    ('non-existing conversion rate', 'TYR', 100, 5.52),  # bug with missing conversion rates
])
def test_money_conversion(test_name, currency, init_amount, converted_amount):
    body = payment.custom_payment(purchase=123, amount=init_amount, currency=currency)
    api.create_payment(body)
    api.process_payments()
    last_payments = api.get_payments().body[-1]
    delayed_assert.expect(last_payments.currency == "EUR", f"Currency {last_payments.currency} is not converted to EUR")
    delayed_assert.expect(last_payments.processed == 1, "Payment is not processed")
    delayed_assert.expect(last_payments.amount == converted_amount,
                          f"Converted amount {converted_amount} is invalid, actual is {last_payments.amount}")
    delayed_assert.assert_expectations()


def test_skip_invalid_payments_processing():
    init_amount = 10.2
    currency = "pjgerkg"
    body = payment.custom_payment(purchase=123, amount=init_amount, currency=currency)
    api.create_payment(body)
    api.process_payments()
    last_payments = api.get_payments().body[-1]
    delayed_assert.expect(last_payments.amount == init_amount, "Amount is changed")
    delayed_assert.expect(last_payments.processed == 0, "Payment with invalid currency is processed")
    delayed_assert.expect(last_payments.currency == currency, "Invalid currency is changed")
    delayed_assert.assert_expectations()
