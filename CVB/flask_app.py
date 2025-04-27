# CVB/flask_app.py

import os
import asyncio
from flask import Flask, request, jsonify
from CVB import config
from CVB.bot import dp
from aiogram import types

app = Flask(__name__)
app.secret_key = config.FLASK_SECRET_KEY

# --- TELEGRAM WEBHOOK ---
@app.route('/webhook/telegram', methods=['POST'])
def telegram_webhook():
    update = types.Update.to_object(request.get_json())
    asyncio.run(dp.process_update(update))
    return jsonify({"status": "ok"}), 200

# --- PAYMENT WEBHOOKS ---
@app.route('/webhook/flutterwave', methods=['POST'])
def flutterwave_webhook():
    data = request.get_json()
    # handle payment webhook
    return jsonify({"status": "success"}), 200

@app.route('/webhook/paystack', methods=['POST'])
def paystack_webhook():
    data = request.get_json()
    # handle payment webhook
    return jsonify({"status": "success"}), 200

@app.route('/webhook/nowpayments', methods=['POST'])
def nowpayments_webhook():
    data = request.get_json()
    # handle payment webhook
    return jsonify({"status": "success"}), 200

# --- HOME ---
@app.route('/')
def index():
    return "CryptoValBot Web API is live!", 200
