from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, FileResponse
from .models import Order, OrderItem

@login_required
def order_history_view(request):
    orders = Order.objects.filter(buyer=request.user, status='Completed').order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def download_product_file(request, product_id):
    # Vérifier que l'acheteur a bien acheté ce produit dans une commande complétée
    has_purchased = OrderItem.objects.filter(
        order__buyer=request.user,
        order__status='Completed',
        product_id=product_id
    ).exists()

    if not has_purchased and not request.user.is_staff:
        raise Http404("Vous n'avez pas acheté ce produit ou la commande n'est pas validée.")

    from products.models import Product
    product = get_object_or_404(Product, id=product_id)
    
    if product.file:
        return FileResponse(product.file.open(), as_attachment=True)
    raise Http404("Fichier introuvable.")