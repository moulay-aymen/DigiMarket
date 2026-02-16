# services.py
from django.conf import settings
from chargily_pay import ChargilyClient
from .models import AmountCheckout

client = ChargilyClient(
    secret=settings.CHARGILY_SECRET,
    key=settings.CHARGILY_KEY,
    url=settings.CHARGILY_URL,
)


def create_checkout(checkout: AmountCheckout) -> AmountCheckout:
    response = client.create_checkout(checkout=checkout.to_entity())

    checkout.entity_id = response["id"]
    checkout.checkout_url = response["checkout_url"]
    checkout.save()

    return checkout
