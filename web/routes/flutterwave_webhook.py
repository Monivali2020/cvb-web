from flask import Blueprint, request, jsonify
from CVB.models.wallet_model import update_wallet_balance
from CVB.utils.flutterwave import verify_payment

flutterwave_bp = Blueprint("flutterwave_webhook", __name__)

@flutterwave_bp.route("/webhook/flutterwave", methods=["POST"])
def flutterwave_webhook():
    data = request.json

    if not data:
        return jsonify({"status": "error", "message": "Invalid request"}), 400

    # Validate transaction ID
    transaction_id = data.get("data", {}).get("id")
    if not transaction_id:
        return jsonify({"status": "error", "message": "Missing transaction ID"}), 400

    # Verify transaction with Flutterwave
    verification = verify_payment(str(transaction_id))
    status = verification.get("data", {}).get("status")
    amount = float(verification.get("data", {}).get("amount", 0))
    email = verification.get("data", {}).get("customer", {}).get("email")

    if status == "successful" and email:
        try:
            user_id = int(email.split("_")[1])
            update_wallet_balance(user_id, amount)
            return jsonify({"status": "success", "message": "Wallet funded"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "error", "message": "Invalid payment status"}), 400