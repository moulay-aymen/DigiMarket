from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('history/', views.order_history_view, name='order_history'),
    path('download/<int:product_id>/', views.download_product_file, name='download_file'),
]