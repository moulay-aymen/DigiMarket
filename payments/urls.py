from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('checkout/<int:product_id>/', views.initiate_checkout, name='initiate_checkout'),
    path('callback/<int:order_id>/', views.payment_callback, name='payment_callback'),
    path('withdrawal/request/', views.request_withdrawal, name='request_withdrawal'),
    path('success/<int:order_id>/', views.payment_success_view, name='payment_success'),
]