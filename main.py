from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = "7594223959:AAEoJ31lf-L5hlRkCyqtIXxIzPxR0teXAl8"
CHATGPT_API_KEY = "d521c890-1b75-11f0-a0dc-f72cb9db58e1"

# Home route
@app.route('/')
def home():
    return "DreamX_11 Bot is Live!"

# Webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text.lower().startswith("/team"):
            send_message(chat_id, "Dream11 team coming soon! (ChatGPT + Live data feature)")
        elif text.lower().startswith("/start"):
            send_message(chat_id, "Welcome to DreamXpert 11! Type /team to get started.")
        else:
            send_message(chat_id, "I am DreamX_11 Bot! Type /team to get your fantasy team.")

    return "OK", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
