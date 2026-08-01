from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('vendor/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/product/add/', views.vendor_product_create, name='product_create'),
    path('vendor/product/edit/<int:pk>/', views.vendor_product_update, name='product_update'),
    path('vendor/product/delete/<int:pk>/', views.vendor_product_delete, name='product_delete'),
]