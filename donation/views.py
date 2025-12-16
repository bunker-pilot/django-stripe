from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# Create your views here.

# donation page

def my_donation(request):
    return render(request, "donation/home.html")

# payment success

def payment_success(request):
    return render(request , "donation/payment_success.html")

#payment failed 
def payment_fail(request):
    return render(request , "donation/payment_fail.html")
