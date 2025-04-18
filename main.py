from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = "7594223959:AAEoJ31lf-L5hlRkCyqtIXxIzPxR0teXAl8"
CHATGPT_URL = "https://free.churchless.tech/v1/chat/completions"  # FREE endpoint

# Send message to Telegram
def send_message(chat_id, text, parse_mode="Markdown"):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    requests.post(url, json=payload)

# Home route
@app.route('/')
def home():
    return "DreamX_11 Bot is Online - Dream Big, Win Bigger!"

# Telegram webhook handler
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("Received data:", data)

        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "").strip().lower()

            commands = {
                "/start": welcome_text(),
                "/team": generate_chatgpt_response(team_prompt()),
                "/pitch": pitch_weather_report(),
                "/captain": generate_chatgpt_response(captain_prompt()),
                "/tips": generate_chatgpt_response(tips_prompt()),
                "/preview": generate_chatgpt_response(preview_prompt())
            }

            response = commands.get(text, "❌ Please type /team, /pitch, /captain, /tips or /preview")
            send_message(chat_id, response)

        return "OK", 200

    except Exception as e:
        print("Error in webhook:", e)
        return "Internal Server Error", 500

# ChatGPT response generator (NO API KEY needed)
def generate_chatgpt_response(prompt):
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    try:
        res = requests.post(CHATGPT_URL, json=payload, timeout=15)
        data = res.json()
        print("LLM Response:", data)
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error getting response: {e}"

# Prompts
def team_prompt():
    return (
        "Generate a Dream11 fantasy team for today's IPL match. Include:\n"
        "- WK, BAT, AR, BOWL\n"
        "- Captain & Vice Captain\n"
        "- Form (last 5 matches)\n"
        "- Country flags & emojis\n"
        "- Budget used\n"
        "- Smart formatting for Telegram"
    )

def captain_prompt():
    return (
        "Suggest the top 3 Captain & Vice Captain picks for today's IPL match.\n"
        "Explain with pitch, form, opposition, and include emoji formatting."
    )

def tips_prompt():
    return (
        "Give match prediction & fantasy tips for today's IPL game:\n"
        "- Who might win?\n"
        "- Key fantasy players\n"
        "- Pitch/weather effects\n"
        "- Strategy tips"
    )

def preview_prompt():
    return (
        "Short preview for today's IPL match:\n"
        "- Head-to-head\n"
        "- Top batters/bowlers\n"
        "- Probable openers\n"
        "- Which team has an edge"
    )

# Static pitch report
def pitch_weather_report():
    return (
        "🏟 *Venue:* M. Chinnaswamy Stadium, Bengaluru\n"
        "🧱 *Pitch:* Flat, high scoring – Avg 1st Innings: 190+\n"
        "🌤 *Weather:* Clear skies, 32°C, no rain\n"
        "✅ *Fantasy Tip:* Focus on top-order batters & death bowlers"
    )

# Welcome message
def welcome_text():
    return (
        "*Welcome to DreamX_11 – Your Fantasy Cricket Guru!*\n\n"
        "Use these commands:\n"
        "▶️ /team – AI-based Dream11 Team\n"
        "🌦 /pitch – Pitch & Weather\n"
        "🎯 /captain – C/VC Picks\n"
        "📊 /preview – Match Preview\n"
        "🔥 /tips – Expert Fantasy Tips\n\n"
        "_Powered by AI + Cricket Stats + Your Luck_"
    )

# Run server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
