from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_donation , name= "home"),
    path("payment-success/"  , views.payment_success , name = "payment-success" ),
    path("payment-fail/" , views.payment_fail , name = "payment-fail")
]
