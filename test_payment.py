import os
import django
import requests
import uuid


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyPro.settings")
django.setup()

from django.contrib.auth.models import User
from MyApp.models import Product, Order, Profile

# =====================================
# 1) إنشاء بيانات اختبارية
# =====================================
chargily_id = f"chk_local_{uuid.uuid4().hex[:6]}"
buyer = User.objects.first()           # مستخدم موجود
product = Product.objects.first()      # منتج موجود

# احسب العمولة مثلاً 20%
total_amount = 1000
commission = total_amount * 0.2
seller_amount = total_amount - commission

order = Order.objects.create(
    buyer=buyer,
    product=product,
    total_amount=total_amount,
    commission=commission,
    seller_amount=seller_amount,
    chargily_id=chargily_id,
    status="PAN",   # Pending
)


print("Order created with ID:", order.chargily_id)

# =====================================
# 2) إرسال Webhook وهمي
# =====================================

data = {
    "type": "checkout.paid",
    "id": chargily_id
}


r = requests.post("http://127.0.0.1:8000/webhook/chargily/", data=data)
print("Webhook response:", r.text)
