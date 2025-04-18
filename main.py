from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = "7594223959:AAEoJ31lf-L5hlRkCyqtIXxIzPxR0teXAl8"
CHATGPT_API_KEY = "d521c890-1b75-11f0-a0dc-f72cb9db58e1"

def send_message(chat_id, text, parse_mode="Markdown"):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    requests.post(url, json=payload)

@app.route('/')
def home():
    return "DreamX_11 Bot is Online - Dream Big, Win Bigger!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "").lower()

        if "/start" in text:
            send_message(chat_id, welcome_text())
        elif "/team" in text:
            send_message(chat_id, generate_chatgpt_response(team_prompt()))
        elif "/pitch" in text:
            send_message(chat_id, pitch_weather_report())
        elif "/captain" in text:
            send_message(chat_id, generate_chatgpt_response(captain_prompt()))
        elif "/tips" in text:
            send_message(chat_id, generate_chatgpt_response(tips_prompt()))
        elif "/preview" in text:
            send_message(chat_id, generate_chatgpt_response(preview_prompt()))
        else:
            send_message(chat_id, "Please type /team, /pitch, /captain, /tips or /preview")

    return "OK", 200

# PROMPTS SECTION
def team_prompt():
    return (
        "Generate a Dream11 fantasy cricket team for today's IPL match. Include:\n"
        "- Player categories: WK, BAT, AR, BOWL\n"
        "- Captain (C) & Vice Captain (VC)\n"
        "- Player form (last 5 matches)\n"
        "- Country flags & emojis\n"
        "- Team cost and balance\n"
        "- Smart formatting for Telegram"
    )

def captain_prompt():
    return (
        "Suggest the top 3 Captain & Vice Captain picks for today's IPL Dream11 match.\n"
        "Include reason (form, pitch, matchup) + emoji formatting."
    )

def tips_prompt():
    return (
        "Give match prediction and tips for today's IPL match. Mention:\n"
        "- Winning team prediction\n"
        - Key players to watch\n"
        - Pitch & weather impact\n"
        "- Strategy tips for fantasy users"
    )

def preview_prompt():
    return (
        "Give a short, exciting match preview for today's IPL match.\n"
        "- Head-to-head record\n"
        "- Top batters & bowlers\n"
        "- Probable opening pairs\n"
        "- Who has edge today"
    )

# STATIC PITCH REPORT
def pitch_weather_report():
    return (
        "🏟 *Venue:* M. Chinnaswamy Stadium, Bengaluru\n"
        "🧱 *Pitch:* Flat and high scoring – Average 1st innings score: 190+\n"
        "🌤 *Weather:* Clear skies, 32°C, no rain\n"
        "✅ *Fantasy Tip:* Pick top-order batters and death-over bowlers"
    )

# CHATGPT FETCH FUNCTION
def generate_chatgpt_response(prompt):
    headers = {
        "Authorization": f"Bearer {CHATGPT_API_KEY}"
    }
    res = requests.post("https://api.chatanywhere.tech/v1/chat/completions", json={
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }, headers=headers)

    return res.json()["choices"][0]["message"]["content"]

# WELCOME MESSAGE
def welcome_text():
    return (
        "*Welcome to DreamX_11 – Your Fantasy Cricket Guru!*\n\n"
        "Use these commands:\n"
        "▶️ /team – Get today's best AI Dream11 team\n"
        "🌦 /pitch – Pitch & Weather insights\n"
        "🎯 /captain – C/VC recommendations\n"
        "📊 /preview – Match Preview & H2H\n"
        "🔥 /tips – Pro fantasy advice\n\n"
        "_Powered by ChatGPT + Cricket Stats + Your Luck_"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
