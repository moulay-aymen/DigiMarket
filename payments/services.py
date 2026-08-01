import requests
from django.conf import settings

def initialize_slickpay_payment(order, amount, callback_url):
    """
    Intégration de l'API de paiement SlickPay (v2).
    """
    base_url = "https://devapi.slick-pay.com/api/v2"  # passe à prodapi.slick-pay.com en prod
    api_url = f"{base_url}/users/invoices"

    payload = {
        "amount": float(amount),
        "url": callback_url,   # URL de retour après paiement
        # ⚠️ à vérifier dans ton dashboard SlickPay : d'autres champs sont
        # parfois requis (ex: mode, items, etc.) — regarde l'onglet "API"
        # de ton compte, la structure exacte peut varier selon ton offre.
    }
    headers = {
        "Accept": "application/json",              # header manquant dans ta version
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.SLICKPAY_API_KEY}",
    }
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        data = response.json()
        if response.status_code == 200 and data.get("success") == 1:
            return data.get("url")          # ✅ bon nom de champ
        else:
            print("Erreur SlickPay:", data)  # log pour debug au lieu de pass silencieux
    except requests.RequestException as e:
        print("Erreur réseau SlickPay:", e)
    return None