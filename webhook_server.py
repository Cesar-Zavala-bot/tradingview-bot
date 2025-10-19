from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# === CARGAR VARIABLES DE ENTORNO ===
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# === CONFIGURAR FLASK ===
app = Flask(__name__)

# === FUNCIÓN PARA ENVIAR MENSAJE A TELEGRAM ===
def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"⚠️ Error enviando mensaje a Telegram: {e}")

# === ENDPOINT PARA RECIBIR ALERTAS DE TRADINGVIEW ===
@app.route('/alert', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    print("📩 Alerta recibida:", data)

    symbol = data.get("symbol", "N/A")
    action = data.get("action", "N/A")
    price = data.get("price", "N/A")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    mensaje = f"""
🚨 *Nueva señal recibida desde TradingView* 🚨

📊 *Símbolo:* {symbol}
📈 *Acción:* {action}
💵 *Precio:* {price}
🕒 *Hora:* {timestamp}
"""

    print(mensaje)
    send_telegram_message(mensaje)

    return jsonify({"status": "ok"})

# === EJECUTAR SERVIDOR ===
if __name__ == '__main__':
    print("🚀 Servidor Flask escuchando alertas en http://127.0.0.1:5000/alert")
    app.run(host='0.0.0.0', port=5000)
