import os
import requests

SECRET = os.getenv("FLUTTERWAVE_SECRET_KEY")
BASE_URL = os.getenv("BASE_URL", "")

def create_invoice(amount_naira: float, user_id: int) -> dict:
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer {SECRET}",
        "Content-Type": "application/json"
    }
    payload = {
        "tx_ref": f"cvb_{user_id}_{int(__import__('time').time())}",
        "amount": str(amount_naira),
        "currency": "NGN",
        "redirect_url": f"{BASE_URL}/webhook/flutterwave",
        "customer": {"email": f"user_{user_id}@example.com"},
    }
    return requests.post(url, json=payload, headers=headers).json()

def verify_payment(transaction_id: str) -> dict:
    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {"Authorization": f"Bearer {SECRET}"}
    return requests.get(url, headers=headers).json()