def send_telegram_message(message):
    import requests, os
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    print(f"🔍 Enviando a Telegram: {data}")
    try:
        r = requests.post(url, data=data)
        print("📡 Respuesta de Telegram:", r.status_code, r.text)
    except Exception as e:
        print(f"⚠️ Error enviando mensaje a Telegram: {e}")


