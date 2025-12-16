from django.shortcuts import render, redirect
from django.urls import reverse_lazy
import stripe
from django.conf import settings
# Create your views here.

# donation page

def my_donation(request):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY 
    session = stripe.checkout.Session.create(
    line_items=[{
      'price' :"price_1Sf4IhHFCVFwqm5wQHsaawvj",
      'quantity': 1,
    }],
    mode='payment',
    success_url=request.build_absolute_url( reverse_lazy("payment-success")) + "?session_id={CHECKOUT_SESSION_ID}",
    cancel_url = request.build_absolute_url(reverse_lazy("payment-fail"))
  )

    return render(request, "donation/home.html")

# payment success

def payment_success(request):
    return render(request , "donation/payment_success.html")

#payment failed 
def payment_fail(request):
    return render(request , "donation/payment_fail.html")
