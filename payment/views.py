import json

import stripe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from basket.basket import Basket
from orders.views import payment_confirmation


@login_required
def BasketView(request):
    basket = Basket(request)
    total = str(basket.get_subtotal_price())
    total = total.replace(".", "")
    total = int(total)

    stripe.api_key = "sk_test_51MuOeFECwywCrXWAjIweLWhcXYSZGcHjRe2ZezAsHEb5K0arcsw2NIz0yq6DmXRuO4Os0vW1gWwDxGx9fj6v4JRU00MaOKDg3N"
    intent = stripe.PaymentIntent.create(
        amount=total, currency="gbp", metadata={"userid": request.user.id}
    )

    return render(request, "payment/home.html", {"client_secret": intent.client_secret})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)
    print()
    if event.type == "payment_intent.succeeded":
        payment_confirmation(event.data.object.client_secret)
    else:
        print("Unhandled event type {}".format(event.type))

    return HttpResponse(status=200)


def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')