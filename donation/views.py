from django.shortcuts import render, redirect
from django.urls import reverse_lazy
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Donation
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
                    "unit_amount": int(amount) * 100,
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
    session_id = request.GET.get("session_id")

    if not session_id:
        messages.error(request, "No offering was detected.")
        return redirect("home")

    donation = Donation.objects.filter(
        session_id=session_id,
        confirmed=True,
    ).first()

    if donation:
        messages.success(
            request,
            "✨ The Sanctuary has received your offering."
        )
    else:
        messages.warning(
            request,
            "🔮 Your offering is being verified by the arcane council."
        )

    return render(request, "donation/payment_success.html")


#payment failed 
def payment_fail(request):
    return render(request , "donation/payment_fail.html")

@csrf_exempt
def stripe_webhook(request):

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(
            payload = payload, sig_header=sig_header,secret=endpoint_secret
        )
    except ValueError:
        messages.error(request, "Something went wrong")
        return HttpResponse(status = 400)
    except stripe.error.SignatureVerificationError:
        messages.error(request, "Something went wrong")
        return HttpResponse(status = 400)

    if event["type"] =="checkout.session.completed":
        session = event["data"]["object"]
        handle_success_pay(session)

    return HttpResponse(status =200)

def handle_success_pay(session):
    session_id = session.get("id") 
    amount = session["amount_total"] /100
    email = session.get("customer_details", {}).get("email")
    Donation.objects.update_or_create(
        session_id = session_id , amount= amount , email = email, confirmed = True
    )
    print("payment_success")