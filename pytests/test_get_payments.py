import delayed_assert
import pytest

from clients.api import ApiClient
from model.payments import CreatePayment, GetPayment

api = ApiClient()
payment = CreatePayment()


@pytest.fixture(autouse=True)
def cleanup():
    yield
    last_payment = api.get_payments().body[-1]
    api.delete_payment(last_payment.payment_id)


def test_get_created_payment():
    body = payment.valid_payment()
    api.create_payment(body)
    last_payment = api.get_payments().body[-1]
    expected_payment = GetPayment().convert_from_request(payment.from_json(body), api.user, last_payment.payment_id)
    assert expected_payment.to_json() == last_payment.to_json()


def test_get_processed_payment():
    body = payment.valid_payment()
    api.create_payment(body)
    api.process_payments()
    last_payment = api.get_payments().body[-1]
    expected_payment = GetPayment().convert_from_request(payment.from_json(body), api.user, last_payment.payment_id, 1)
    assert expected_payment.to_json() == last_payment.to_json()


def test_always_same_payments_order():
    api.create_payment(payment.valid_payment())
    payments_resp_1 = api.get_payments()
    payments_resp_2 = api.get_payments()
    delayed_assert.expect(payments_resp_1.raw_body == payments_resp_2.raw_body)
    delayed_assert.expect(payments_resp_1.status == 200)
    delayed_assert.expect(payments_resp_2.status == 200)
    delayed_assert.assert_expectations()
