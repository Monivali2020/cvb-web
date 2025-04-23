import os
import requests

SECRET = os.getenv("PAYSTACK_SECRET_KEY")
BASE_URL = os.getenv("BASE_URL", "")

def create_invoice(amount_naira: int, email: str = None) -> dict:
    url = "https://api.paystack.co/transaction/initialize"
    headers = {"Authorization": f"Bearer {SECRET}"}
    payload = {
        "amount": amount_naira * 100,
        "currency": "NGN",
        "callback_url": f"{BASE_URL}/webhook/paystack",
        "metadata": {"user_id": None if email is None else email}
    }
    return requests.post(url, json=payload, headers=headers).json()

def verify_payment(reference: str) -> dict:
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization": f"Bearer {SECRET}"}
    return requests.get(url, headers=headers).json()