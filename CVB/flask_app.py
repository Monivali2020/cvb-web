# flask_app.py
from flask import Flask, request, jsonify
from CVB import config

app = Flask(__name__)
app.secret_key = config.FLASK_SECRET_KEY

@app.route('/')
def index():
    return "CryptoValBot Web API is live!", 200

# === WEBHOOK ROUTES ===
@app.route('/webhook/flutterwave', methods=['POST'])
def flutterwave_webhook():
    data = request.get_json()
    print("Received Flutterwave Webhook:", data)
    return jsonify({"status": "success"}), 200

@app.route('/webhook/paystack', methods=['POST'])
def paystack_webhook():
    data = request.get_json()
    print("Received Paystack Webhook:", data)
    return jsonify({"status": "success"}), 200

@app.route('/webhook/nowpayments', methods=['POST'])
def nowpayments_webhook():
    data = request.get_json()
    print("Received NowPayments Webhook:", data)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT)