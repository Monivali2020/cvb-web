import os
from flask import Flask, request, jsonify
# from CVB.models.wallet_model import update_wallet_balance
# from web.routes.flutterwave_webhook import flutterwave_bp
# from web.routes.nowpayments_webhook import nowpayments_bp
# from web.routes.paystack_webhook import paystack_bp

app = Flask(__name__)

# Register Webhook Blueprints
# app.register_blueprint(flutterwave_bp)
# app.register_blueprint(nowpayments_bp)
# app.register_blueprint(paystack_bp)

# Health check route (IMPORTANT)
@app.route("/")
def index():
    return "CryptoValBot Webhook Server is live!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))