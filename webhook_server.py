from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# === Configura tus credenciales de Telegram ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "AQUI_VA_TU_TOKEN")
CHAT_ID = os.getenv("CHAT_ID", "AQUI_VA_TU_CHAT_ID")

# === Función para enviar mensajes a Telegram ===
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"❌ Error enviando a Telegram: {e}")

# === Endpoint principal para recibir alertas de TradingView ===
@app.route('/alert', methods=['POST'])
def alert():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON recibido"}), 400

    symbol = data.get("symbol", "N/A")
    action = data.get("action", "N/A")
    price = float(data.get("price", 0))

    # Calcular TP y SL dinámicos
    if action == "BUY":
        take_profit = round(price * 1.01, 5)
        stop_loss = round(price * 0.99, 5)
    elif action == "SELL":
        take_profit = round(price * 0.99, 5)
        stop_loss = round(price * 1.01, 5)
    else:
        take_profit = stop_loss = 0

    mensaje = f"""
📊 *Alerta TradingView*
💹 Par: `{symbol}`
🧭 Acción: *{action}*
💰 Precio: `{price}`
🎯 Take Profit: `{take_profit}`
🛑 Stop Loss: `{stop_loss}`
"""

    print("📩 Señal procesada:", mensaje)
    send_telegram_message(mensaje)

    return jsonify({"status": "ok"})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

