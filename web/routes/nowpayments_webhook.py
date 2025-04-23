from flask import Blueprint, request, jsonify
from CVB.models.wallet_model import update_wallet_balance

nowpayments_bp = Blueprint("nowpayments_webhook", __name__)

@nowpayments_bp.route('/webhook/nowpayments', methods=["POST"])
def nowpayments_webhook():
    data = request.json
    if data.get("payment_status") == "finished":
        try:
            user_id = int(data.get("order_id").replace("CVB_", ""))
            amount_received = float(data.get("actually_paid"))
            currency = data.get("pay_currency")

            update_wallet_balance(user_id, amount_received)
            print(f"User {user_id} deposited {amount_received} {currency.upper()} via NOWPayments")
        except Exception as e:
            print("NOWPayments Error:", str(e))

    return jsonify({"code": 200})