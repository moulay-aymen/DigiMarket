from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import WithdrawalRequest
from orders.models import Order, OrderItem
from products.models import Product
from .services import initialize_slickpay_payment
import decimal

@login_required
def initiate_checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Créer la commande en attente
    order = Order.objects.create(
        buyer=request.user,
        total_amount=product.price,
        status='Pending'
    )
    OrderItem.objects.create(
        order=order,
        product=product,
        price=product.price
    )

    callback_url = request.build_absolute_uri(f"/payments/callback/{order.id}/")
    payment_url = initialize_slickpay_payment(order, product.price, callback_url)

    if payment_url:
        return redirect(payment_url)
    
    # Mode simulation/fallback si l'API SlickPay externe n'est pas joignable en local
    return redirect('payments:payment_success', order_id=order.id)

@login_required
def payment_callback(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    if order.status != 'Completed':
        order.status = 'Completed'
        order.save()

        # Traitement des ventes et répartition financière (90% vendeur, 10% plateforme)
        for item in order.items.all():
            product = item.product
            product.sales_count += 1
            product.save()

            vendor_profile = product.vendor.profile
            commission = item.price * Decimal('0.10')
            vendor_earnings = item.price - commission
            vendor_profile.balance += vendor_earnings
            vendor_profile.save()

        messages.success(request, "Paiement effectué avec succès ! Votre produit est disponible.")
    return redirect('orders:order_history')

@login_required
def request_withdrawal(request):
    if not request.user.is_vendor:
        messages.error(request, "Accès réservé aux vendeurs.")
        return redirect('products:home')

    profile = request.user.profile
    now = timezone.now()

    # Règle des 14 jours
    if profile.last_withdrawal_date:
        next_allowed_date = profile.last_withdrawal_date + timedelta(days=14)
        if now < next_allowed_date:
            messages.error(request, f"Vous devez attendre jusqu'au {next_allowed_date.strftime('%d/%m/%Y')} pour effectuer une nouvelle demande de retrait.")
            return redirect('dashboard:vendor_dashboard')

    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
        except decimal.InvalidOperation:
            amount = Decimal('0')

        # Règle du retrait minimum : 500 DZD
        if amount < Decimal('500'):
            messages.error(request, "Le montant minimum de retrait est de 500 DZD.")
        elif amount > profile.balance:
            messages.error(request, "Solde insuffisant pour ce montant.")
        else:
            WithdrawalRequest.objects.create(
                vendor=request.user,
                amount=amount,
                rip=profile.rip or "Non renseigné"
            )
            profile.balance -= amount
            profile.last_withdrawal_date = now
            profile.save()
            messages.success(request, "Demande de retrait enregistrée avec succès.")
            return redirect('dashboard:vendor_dashboard')

    return render(request, 'payments/request_withdrawal.html', {'profile': profile})

from django.shortcuts import render
from orders.models import Order

def payment_success_view(request, order_id):
    """Vue gérant le retour après un paiement réussi"""
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    context = {'order': order}
    return render(request, 'payments/success.html', context)