from django.shortcuts import render, redirect
from django.urls import reverse_lazy
import stripe
from django.conf import settings
# Create your views here.

# donation page
stripe.api_key = settings.STRIPE_PRIVATE_KEY 
def my_donation(request):
    if request.method == "POST":
      amount = request.POST.get("amount")
      session = stripe.checkout.Session.create(
      payment_method_types=["card"],
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Magical Offering",
                    },
                    "unit_amount": int(amount),
                },
                "quantity": 1,
            }],
      success_url=request.build_absolute_uri( reverse_lazy("payment-success")) + "?session_id={CHECKOUT_SESSION_ID}",
      cancel_url = request.build_absolute_uri(reverse_lazy("payment-fail"))
    )
      return redirect(session.url)
    return render(request, "donation/home.html")

# payment success

def payment_success(request):
    return render(request , "donation/payment_success.html")

#payment failed 
def payment_fail(request):
    return render(request , "donation/payment_fail.html")
