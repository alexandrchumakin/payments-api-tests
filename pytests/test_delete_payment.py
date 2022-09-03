import pytest
from delayed_assert import delayed_assert

from clients.api import ApiClient
from model.payments import CreatePayment

api = ApiClient()
payment = CreatePayment()


@pytest.mark.parametrize(('test_name', 'purchase', 'amount', 'currency'), [
    ('valid', 146, 22.12, "EUR"),
    ('invalid', 147, 21, "Ab1!"),
])
def test_delete_single_payment(test_name, purchase, amount, currency):
    body = payment.custom_payment(purchase=purchase, amount=amount, currency=currency)
    api.create_payment(body)
    last_payment = api.get_payments().body[-1]
    response = api.delete_payment(last_payment.payment_id)
    delayed_assert.expect(response.status == 200, f"Invalid status code {response.status}")
    delayed_assert.expect(response.body['deleted'] == 1, f"Deleted number {response.body['deleted']} is wrong")

    # get new payments list to make sure payment is not there
    new_last_payment = api.get_payments().body[-1]
    delayed_assert.expect(last_payment.payment_id != new_last_payment.payment_id, "Payment is not removed from list")
    delayed_assert.assert_expectations()


def test_delete_non_existing_payment():
    response = api.delete_payment(458435897345)
    delayed_assert.expect(response.status == 200, f"Invalid status code {response.status}")
    delayed_assert.expect(response.body['deleted'] == 0, f"Deleted number {response.body['deleted']} is wrong")
    delayed_assert.assert_expectations()


def test_delete_multiple_payments():
    api.create_payment(payment.valid_payment())
    api.create_payment(payment.custom_payment(135, 12.12, "USD"))
    all_payments = api.get_payments().body
    api.delete_payment(all_payments[-1].payment_id)
    api.delete_payment(all_payments[-2].payment_id)
    fresh_get_resp = api.get_payments()
    delayed_assert.expect(fresh_get_resp.status == 200, f"Invalid status code {fresh_get_resp.status}")
    delayed_assert.expect(all_payments[-1].payment_id not in fresh_get_resp.body)
    delayed_assert.expect(all_payments[-2].payment_id not in fresh_get_resp.body)
    delayed_assert.assert_expectations()
