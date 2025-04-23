from flask import Blueprint, request, jsonify
from CVB.models.wallet_model import update_wallet_balance

paystack_bp = Blueprint("paystack_webhook", __name__)

@paystack_bp.route("/webhook/paystack", methods=["POST"])
def paystack_webhook():
    data = request.json
    try:
        user_id = int(data["data"]["metadata"]["user_id"])
        amount = float(data["data"]["amount"]) / 100

        update_wallet_balance(user_id, amount)
        print(f"User {user_id} deposited NGN {amount} via Paystack")
    except Exception as e:
        print("Paystack Webhook Error:", str(e))

    return jsonify({"status": "success"}), 200