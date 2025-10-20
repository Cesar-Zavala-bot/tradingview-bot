from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# === Variables de entorno ===
TELEGRAM_TOKEN = os.getenv("8336480592:AAHWOaaVtlTxRGh8NDzzGSR968oBw7kNMdw")
CHAT_ID = os.getenv("5667629296")

# === Función para enviar mensaje a Telegram ===
def send_telegram_message(text):
    print(f"🧩 Usando TOKEN={TELEGRAM_TOKEN} y CHAT_ID={CHAT_ID}")
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("❌ Faltan variables de entorno TELEGRAM_TOKEN o CHAT_ID")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}

    try:
        response = requests.post(url, data=data)
        print(f"✅ Telegram status: {response.status_code}, respuesta: {response.text}")
    except Exception as e:
        print(f"⚠️ Error enviando mensaje a Telegram: {e}")


# === Ruta Webhook ===
@app.route('/alert', methods=['POST'])
def alert():
    data = request.get_json()
    print("📩 Alerta recibida:", data)

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

# === Inicio del servidor ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

