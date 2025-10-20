from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(text):
    print(f"Intentando enviar mensaje a Telegram con TOKEN={TELEGRAM_TOKEN} y CHAT_ID={CHAT_ID}")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=data)
        print(f"Telegram status: {response.status_code}, respuesta: {response.text}")
    except Exception as e:
        print(f"⚠️ Error enviando mensaje a Telegram: {e}")

@app.route("/alert", methods=["POST"])
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# === Inicio del servidor ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


