from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .stripe_service import StripeService


class ChargeView(APIView):

    # create charge
    def post(self, request):
        charge = StripeService().create_charge(**request.data)
        return Response(charge.data, status=charge.status)

    # get charge or list of charges
    def get(self, request, charge_id=None):
        if charge_id:
            charge = StripeService().retrieve_charge(charge_id)
        else:
            charge = StripeService().list_charge(**request.data)

        return Response(charge.data, status=charge.status)

    # capture charge for two-step payment case
    def put(self, request, charge_id=None):
        charge = StripeService().capture_charge(charge_id)
        return Response(charge.data, status=charge.status)


class CustomerView(APIView):

    # create customer
    def post(self, request):
        customer = StripeService().create_cutomer(**request.data)
        return Response(customer.data, status=customer.status)


class ProductView(APIView):

    # create product
    def post(self, request):
        product = StripeService().create_product(**request.data)
        return Response(product.data, status=product.status)


class PlanView(APIView):

    # create plan
    def post(self, request):
        plan = StripeService().create_plan(**request.data)
        return Response(plan.data, status=plan.status)


class SubscriptionView(APIView):

    # create subscription
    def post(self, request):
        subscription = StripeService().create_subscription(**request.data)
        return Response(subscription.data, status=subscription.status)
