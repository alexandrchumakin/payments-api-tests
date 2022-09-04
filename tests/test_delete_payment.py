from delayed_assert import delayed_assert

from clients.api import ApiClient
from model.payments import CreatePayment

api = ApiClient()
payment = CreatePayment()


def test_delete_single_payment():
    created_payment = api.create_payment(payment.valid_payment()).body
    response = api.delete_payment(created_payment['paymentId'])
    delayed_assert.expect(response.status == 204, f"Invalid status code {response.status}")

    # get new payments list to make sure payment is not there
    payment_list = api.get_payments().body
    delayed_assert.expect(not payment_list or created_payment['paymentId'] != payment_list[0]['paymentId'],
                          "Payment is not removed from the list")
    delayed_assert.assert_expectations()


def test_delete_non_existing_payment():
    response = api.delete_payment(458435897345)
    assert response.status == 404


def test_delete_multiple_payments():
    payment1 = api.create_payment(payment.valid_payment()).body
    payment2 = api.create_payment(payment.valid_payment()).body
    api.delete_payment(payment1['paymentId'])
    api.delete_payment(payment2['paymentId'])
    fresh_get_resp = api.get_payments()
    delayed_assert.expect(payment1['paymentId'] not in fresh_get_resp.body)
    delayed_assert.expect(payment2['paymentId'] not in fresh_get_resp.body)
    delayed_assert.assert_expectations()
