import delayed_assert
import pytest

from clients.api import ApiClient
from model.payments import CreatePayment

api = ApiClient()
payment = CreatePayment()
payments_ids = []


@pytest.fixture(autouse=True, scope='session')
def cleanup():
    yield
    [api.delete_payment(p_id) for p_id in payments_ids]


def test_get_created_payment():
    resp = api.create_payment(payment.valid_payment()).body
    payments_ids.append(resp['paymentId'])
    payment_list = api.get_payments().body
    assert resp in payment_list


def test_get_processed_payment():
    resp = api.create_payment(payment.valid_payment()).body
    payments_ids.append(resp['paymentId'])
    api.process_payments()
    payment_list = api.get_payments().body
    assert resp in payment_list


def test_always_same_payments_order():
    create_resp = api.create_payment(payment.valid_payment()).body
    payments_resp_1 = api.get_payments()
    payments_resp_2 = api.get_payments()
    payments_ids.append(create_resp['paymentId'])
    delayed_assert.expect(payments_resp_1.raw_body == payments_resp_2.raw_body)
    delayed_assert.expect(payments_resp_1.status == 200)
    delayed_assert.expect(payments_resp_2.status == 200)
    delayed_assert.assert_expectations()
