from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/buyer/', views.register_buyer, name='register_buyer'),
    path('register/vendor/', views.register_vendor, name='register_vendor'),
    path('profile/', views.profile_view, name='profile'),
    path('favorites/', views.favorites_list, name='favorites'),
    path('toggle_favorite/<int:product_id>/', views.toggle_favorite , name='toggle_favorite'),
]