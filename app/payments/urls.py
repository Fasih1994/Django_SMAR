from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('confirm', views.CreatePayment.as_view(), name='confirm_payment')
]
