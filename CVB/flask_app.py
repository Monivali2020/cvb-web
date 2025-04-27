# CVB/flask_app.py

import os
from flask import Flask
from CVB import config

app = Flask(__name__)
app.secret_key = config.FLASK_SECRET_KEY

# --- HOME (Keep or remove as needed) ---
@app.route('/')
def index():
    return "CryptoValBot Web API is live!", 200