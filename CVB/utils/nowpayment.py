import os
import requests

API_KEY = os.getenv("CVBNPAPI")

def create_invoice(user_id: int, amount: float) -> dict:
    url = "https://api.nowpayments.io/v1/invoice"
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "price_amount": amount,
        "price_currency": "usd",
        "pay_currency": "usdt",
        "order_id": str(user_id),
        "pay_to_email": None
    }
    return requests.post(url, json=payload, headers=headers).json()

def check_invoice_status(invoice_id: str) -> dict:
    url = f"https://api.nowpayments.io/v1/invoice/{invoice_id}"
    headers = {"x-api-key": API_KEY}
    return requests.get(url, headers=headers).json()