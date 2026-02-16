from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home , name='home'),
    path('add/' , views.Add , name='add'),
    path('detal/<int:id>/', views.Detail , name='detail'),
    path('stock/' , views.Stock , name='stock'),
    path('edit/<int:id>/', views.Edit , name='edit'),
    path('delete/<int:id>' , views.Delete , name='delete'),
    path('sign_up/', views.Sign_up , name='sign_up'),
    path('login/' , views.Login , name='login'),
    path('logout/', views.Logout , name='logout'),
    path('profile/', views.My_Profile , name='profile'),
    path('editeProfile/', views.EditProfile , name='editeProfile'),
    path('createProfile/', views.My_Profile , name='createProfile'),
    path('filter/', views.Filter , name='filter'),
    path('pay/<int:product_id>/', views.create_payment , name='payment'),
    path('webhook/chargily/', views.chargily_webhook, name='webhook'),
    path('showProfile/<int:id>/', views.Profile2 , name='profile2'),
    path("download/<int:product_id>/", views.download_product, name="download_product"),
    path('politique/', views.Politique , name='politique'),
]