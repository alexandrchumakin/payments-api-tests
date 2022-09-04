import pytest
from delayed_assert import delayed_assert

from clients.api import ApiClient
from model.payments import CreatePayment

api = ApiClient(user="admin", password="admin")
payment = CreatePayment()
payments_ids = []


@pytest.fixture(autouse=True)
def cleanup():
    yield
    [api.delete_payment(p_id) for p_id in payments_ids]


def test_process_valid_payment():
    create_resp = api.create_payment(payment.valid_payment()).body
    payments_ids.append(create_resp['paymentId'])
    response = api.process_payments()
    delayed_assert.expect(response.body['processed'] >= 1,
                          f"Invalid processed payments number: {response.body['processed']}")
    delayed_assert.expect(response.status == 200, f"Invalid status code {response.status}")
    delayed_assert.assert_expectations()


def test_process_all_payments():
    create_resp_1 = api.create_payment(payment.valid_payment()).body
    create_resp_2 = api.create_payment(payment.valid_payment()).body
    payments_ids.append(create_resp_1['paymentId'])
    payments_ids.append(create_resp_2['paymentId'])
    response = api.process_payments()
    delayed_assert.expect(response.body['processed'] >= 2,
                          f"Invalid processed payments number: {response.body['processed']}")

    # get all payments to check processing
    all_payment = api.get_payments().body
    [delayed_assert.expect(p['processed'] == 1, "Payment is not processed") for p in all_payment]
    delayed_assert.assert_expectations()


@pytest.mark.parametrize(('test_name', 'currency', 'init_amount', 'converted_amount'), [
    ('same currency', 'EUR', 10.10, 10.10),
    ('existing conversion rate', 'PHP', 100.22, 5697.90788)
])
def test_money_conversion(test_name, currency, init_amount, converted_amount):
    body = payment.custom_payment(purchase=123, amount=init_amount, currency=currency)
    create_resp = api.create_payment(body).body
    payments_ids.append(create_resp['paymentId'])
    api.process_payments()
    processed_payment = list(filter(lambda p: p['paymentId'] == create_resp['paymentId'], api.get_payments().body))[0]
    delayed_assert.expect(processed_payment['currency'] == "EUR",
                          f"Currency {processed_payment['currency']} is not converted to EUR")
    delayed_assert.expect(processed_payment['processed'] == 1, "Payment is not processed")
    delayed_assert.expect(processed_payment['amount'] == converted_amount,
                          f"Converted amount {converted_amount} is invalid, actual is {processed_payment['amount']}")
    delayed_assert.assert_expectations()


def test_cannot_process_with_non_admin():
    user_api = ApiClient(user="john", password="john")
    user_api.create_payment(payment.valid_payment())
    response = user_api.process_payments()
    assert response.status == 403
