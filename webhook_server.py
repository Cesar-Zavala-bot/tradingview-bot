from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# === Variables de entorno ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("🚀 Iniciando servidor Flask...")
print(f"📦 TELEGRAM_TOKEN: {TELEGRAM_TOKEN[:10] + '...'}" if TELEGRAM_TOKEN else "⚠️ No se encontró TELEGRAM_TOKEN")
print(f"📦 CHAT_ID: {CHAT_ID}" if CHAT_ID else "⚠️ No se encontró CHAT_ID")

# === Función para enviar mensaje a Telegram ===
def send_telegram_message(text):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("❌ Error: faltan TELEGRAM_TOKEN o CHAT_ID")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    print(f"➡️ Enviando mensaje a Telegram: {data}")
    try:
        response = requests.post(url, data=data)
        print(f"📡 Telegram status: {response.status_code}, respuesta: {response.text}")
    except Exception as e:
        print(f"⚠️ Error enviando mensaje a Telegram: {e}")

# === Ruta Webhook ===
@app.route('/alert', methods=['POST'])
def alert():
    data = request.get_json()
    print("📩 Alerta recibida:", data)

    if not data:
        return jsonify({"error": "No data"}), 400

    symbol = data.get("symbol", "Desconocido")
    action = data.get("action", "N/A")
    price = data.get("price", "N/A")

    message = f"""
📊 *Señal recibida desde TradingView*
🔹 Símbolo: {symbol}
📈 Acción: {action}
💰 Precio: {price}
"""
    send_telegram_message(message)
    return jsonify({"status": "ok"})

@app.route('/', methods=['GET'])
def home():
    return "✅ Servidor Flask activo", 200

# === Inicio del servidor ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
