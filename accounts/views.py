from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BuyerSignUpForm, VendorSignUpForm, ProfileUpdateForm, ProfileDetailUpdateForm
from .models import Favorite
from products.models import Product

def register_buyer(request):
    if request.method == 'POST':
        form = BuyerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie en tant qu'acheteur !")
            return redirect('products:home')
    else:
        form = BuyerSignUpForm()
    return render(request, 'accounts/register_buyer.html', {'form': form})

def register_vendor(request):
    if request.method == 'POST':
        form = VendorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie en tant que vendeur !")
            return redirect('dashboard:vendor_dashboard')
    else:
        form = VendorSignUpForm()
    return render(request, 'accounts/register_vendor.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileDetailUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('accounts:profile')
    else:
        user_form = ProfileUpdateForm(instance=request.user)
        profile_form = ProfileDetailUpdateForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        favorite.delete()
        product.favorites_count = max(0, product.favorites_count - 1)
        messages.info(request, "Produit retiré de vos favoris.")
    else:
        product.favorites_count += 1
        messages.success(request, "Produit ajouté à vos favoris.")
    product.save()
    return redirect(request.META.get('HTTP_REFERER', 'products:home'))

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'accounts/favorites_list.html', {'favorites': favorites})