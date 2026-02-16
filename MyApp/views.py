from django.shortcuts import render , redirect , get_object_or_404
from .models import Product , Profile , Images , Order
from .forms import ProductForm , ProfileForm
from django.conf import settings
import json, requests
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login , logout , authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .outils import Calculate_commission 
from django.db.models import Q
import json
# Create your views here.


def Sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
        return render(request , 'sign_up.html' , {'form':form})
    
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username=username , password=password)
        if user is not None:
            login(request , user)
            return redirect('home')
    return render(request, 'login.html' )


def Logout(request):
    logout(request)
    return redirect('sign_up')

def Home(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            search = request.POST['search']
            if search is not None:
                products = Product.objects.filter(
                    Q(name__icontains=search) | Q(desc__icontains=search)
                    ).order_by('-likes')
                return render(request , 'home.html' , {'products':products})          
            else:
                products = Product.objects.all().order_by('-likes')
                return render(request , 'home.html' , {'products' : products})
        else:
            products = Product.objects.all().order_by('-likes')
            return render(request , 'home.html' , {'products' : products})            
    else:
        return redirect('sign_up')
    
@login_required
def Filter(request):
    products = Product.objects.all().order_by('-likes')
    if request.method == 'POST':
        choice = request.POST['choices']
        if choice:
            products = Product.objects.filter(category=choice).order_by('-likes')
        return render(request, 'filter.html' , {'products':products})
    else:
        return render(request, 'filter.html' , {'products':products})
@login_required
def Add(request):
    if not hasattr(request.user, 'profile'):
        return redirect('createProfile')
    if request.method == 'POST':
        form = ProductForm(request.POST , request.FILES)
        images = request.FILES.getlist('images')
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            for i in images:
                Images.objects.create(product=product, image=i)
            return redirect('home')
    else:
        form = ProductForm()
        return render(request , 'add.html' , {'form':form})
    
@login_required
def Detail(request, id):
    product = Product.objects.get(id = id)
    images = Images.objects.filter(product=product)
    product.likes = product.likes + 1
    product.save()
    return render(request , 'detail.html' , {'product':product , 'images':images})

@login_required
def Stock(request):
    if not hasattr(request.user, 'profile'):
        return redirect('createProfile')
    user = request.user
    products = Product.objects.filter(user = user)
    return render(request , 'stock.html' , {'products': products})

@login_required
def Edit(request, id):
    if not hasattr(request.user, 'profile'):
        return redirect('createProfile')
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST , request.FILES , instance=product)
        images = request.FILES.getlist('images')
        if form.is_valid():
            form.save()
            
            if images:
                Images.objects.filter(product=product).delete()
                for i in images:
                    Images.objects.create(product=product , image=i)
            return redirect('stock')
    else:
        form = ProductForm(instance=product)
        images = Images.objects.filter(product=product)
        return render(request , 'edit.html' , {'form': form,'images':images})
    
@login_required
def Delete(request, id):
    if not hasattr(request.user, 'profile'):
        return redirect('createProfile')
    product = Product.objects.get(id =id )
    product.delete()
    return redirect('stock')


@login_required
def My_Profile(request):
    user = request.user
    if hasattr(user , 'profile'):
        profile = Profile.objects.get(user=request.user)
        return render(request, 'profile.html' , {'profile':profile})
    else:
        if request.method == 'POST':
            form = ProfileForm(request.POST , request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = user
                profile.save()
                return redirect('profile')
        else:
            form = ProfileForm()
            return render(request , 'createProfile.html' , {'form':form})


@login_required
def Profile2(request, id):
    product = Product.objects.get(id=id)
    profile = product.user.profile
    return render(request, 'profile2.html' , {'profile':profile})

    
@login_required
def EditProfile(request):
    if not hasattr(request.user, 'profile'):
        return redirect('createProfile')
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES , instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
        return render(request , 'editeProfile.html' , {'form':form})
    
@login_required
def create_payment(request, product_id):
    if not hasattr(request.user, 'profile'):
        return redirect('createProfile')
    product = get_object_or_404(Product, id=product_id)

    commission, seller_amount = Calculate_commission(product.price)

    order = Order.objects.create(
        buyer=request.user,
        product=product,
        total_amount=product.price,
        commission=commission,
        seller_amount=seller_amount,
    )

    response = requests.post(
        "https://pay.chargily.com/api/v2/checkouts",
        headers={
            "Authorization": f"Bearer {settings.CHARGILY_SECRET_KEY}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "amount": int(product.price),
            "currency": "dzd",
            "success_url": "http://127.0.0.1:8000/success/",
            "failure_url": "http://127.0.0.1:8000/fail/",
        },
    )

    if response.status_code != 200:
        print(response.text)
        return HttpResponse("Payment error", status=500)

    data = response.json()["data"]

    order.chargily_id = data["id"]
    order.save()

    return redirect(data["checkout_url"])

@login_required
@csrf_exempt
def chargily_webhook(request):
    if not hasattr(request.user, 'profile'):
        return redirect('createProfile')
    if request.method == "POST":
        chargily_id = request.POST.get("id")
        event_type = request.POST.get("type")

        print("WEBHOOK RECEIVED:", chargily_id, event_type)

        order = Order.objects.filter(chargily_id=chargily_id).first()

        if order and event_type == "checkout.paid":
            order.status = 'PAID'
            order.save()

            seller_profile = Profile.objects.get(user=order.product.user)
            seller_profile.balance += order.seller_amount
            seller_profile.save()

            return JsonResponse({"status": "updated"})

    return JsonResponse({"status": "ignored"})



@login_required
def download_product(request, product_id):
    if not request.user.is_authenticated:
        return HttpResponse("Login required")
    if not hasattr(request.user, 'profile'):
        return redirect('createProfile')
    order = Order.objects.filter(
        buyer=request.user,
        product_id=product_id,
        status='PAID'
    ).first()

    if not order:
        return HttpResponse("You must buy this product")

    product = Product.objects.get(id=product_id)

    return FileResponse(product.file.open(), as_attachment=True)

def Politique(request):
    return render(request , 'politique.html')