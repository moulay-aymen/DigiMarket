from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from orders.models import OrderItem
from payments.models import WithdrawalRequest
from .forms import ProductForm

@login_required
def vendor_dashboard(request):
    if not request.user.is_vendor:
        messages.error(request, "Accès restreint aux vendeurs.")
        return redirect('products:home')

    products = Product.objects.filter(vendor=request.user)
    sales = OrderItem.objects.filter(product__vendor=request.user, order__status='Completed').select_related('order', 'product')
    withdrawals = WithdrawalRequest.objects.filter(vendor=request.user)

    context = {
        'products': products,
        'sales': sales,
        'withdrawals': withdrawals,
        'profile': request.user.profile,
    }
    return render(request, 'dashboard/vendor_dashboard.html', context)

@login_required
def vendor_product_create(request):
    if not request.user.is_vendor:
        return redirect('products:home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.save() # Publication immédiate sans validation admin
            messages.success(request, "Produit publié avec succès.")
            return redirect('dashboard:vendor_dashboard')
    else:
        form = ProductForm()
    return render(request, 'dashboard/product_form.html', {'form': form, 'action': 'Ajouter'})

@login_required
def vendor_product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, vendor=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit mis à jour avec succès.")
            return redirect('dashboard:vendor_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/product_form.html', {'form': form, 'action': 'Modifier'})

@login_required
def vendor_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, vendor=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Produit supprimé avec succès.")
        return redirect('dashboard:vendor_dashboard')
    return render(request, 'dashboard/product_confirm_delete.html', {'product': product})