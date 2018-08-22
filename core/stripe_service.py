from collections import namedtuple
from functools import wraps

import stripe
from django.conf import settings

STRIPE_EXCEPTIONS = (
    stripe.error.CardError,
    stripe.error.InvalidRequestError,
    stripe.error.AuthenticationError,
    stripe.error.APIConnectionError,
    stripe.error.StripeError,
)


Response = namedtuple('Response', 'status data')


def handling_exceptions(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
        except STRIPE_EXCEPTIONS as e:
            return Response(status=e.http_status, data=e.user_message)
        else:
            return Response(status=200, data=result)
    return wrapped


class StripeService:

    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET

    @handling_exceptions
    def create_charge(self, **params):
        return stripe.Charge.create(**params)

    @handling_exceptions
    def retrieve_charge(self, charge_id):
        return stripe.Charge.retrieve(charge_id)

    @handling_exceptions
    def list_charge(self, **params):
        return stripe.Charge.list(**params)

    @handling_exceptions
    def capture_charge(self, charge_id):
        return stripe.Charge.retrieve(charge_id).capture()

    @handling_exceptions
    def create_cutomer(self, **params):
        return stripe.Customer.create(**params)

    @handling_exceptions
    def create_product(self, **params):
        return stripe.Product.create(**params)

    @handling_exceptions
    def create_plan(self, **params):
        return stripe.Plan.create(**params)

    @handling_exceptions
    def create_subscription(self, **params):
        return stripe.Subscription.create(**params)
