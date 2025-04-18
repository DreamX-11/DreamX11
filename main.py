import os
# dreamx_bot.py
import requests
import datetime
from flask import Flask, request
import telegram

# Config
BOT_TOKEN = '7594223959:AAEoJ31lf-L5hlRkCyqtIXxIzPxR0teXAl8'
API_KEY = 'd521c890-1b75-11f0-a0dc-f72cb9db58e1'
CHAT_ID = '1760007944'
bot = telegram.Bot(token=BOT_TOKEN)

app = Flask(__name__)

def get_today_match():
    url = f"https://api.cricapi.com/v1/matches?apikey={API_KEY}&offset=0"
    res = requests.get(url).json()
    for match in res['data']:
        if match['date'].startswith(str(datetime.date.today())) and match['status'] == 'not started':
            return match
    return None

def generate_team(match):
    # Fake team logic for demo (replace with real logic or ML model)
    return {
        "match": f"{match['teams'][0]} vs {match['teams'][1]}",
        "date": match['date'],
        "players": {
            "WK": ["🇮🇳 R. Pant"],
            "BAT": ["🇮🇳 V. Kohli", "🇮🇳 R. Gaikwad", "🇮🇳 S. Gill"],
            "ALL": ["🇮🇳 H. Pandya", "🇮🇳 R. Jadeja"],
            "BOWL": ["🇮🇳 B. Kumar", "🇮🇳 M. Siraj", "🇮🇳 R. Bishnoi"],
        },
        "captain": "V. Kohli",
        "vice_captain": "R. Jadeja",
        "budget": "99.5 Cr"
    }

def format_team_message(team):
    msg = f"🏏 *DreamXpert11 Team* | {team['match']}\n"
    msg += f"🗓️ *Date:* {team['date']}\n💰 *Budget Used:* {team['budget']}\n\n"
    msg += f"🧤 *Wicketkeeper:* {', '.join(team['players']['WK'])}\n"
    msg += f"🏏 *Batters:* {', '.join(team['players']['BAT'])}\n"
    msg += f"⚔️ *All-Rounders:* {', '.join(team['players']['ALL'])}\n"
    msg += f"🎯 *Bowlers:* {', '.join(team['players']['BOWL'])}\n\n"
    msg += f"⭐ *Captain:* {team['captain']}\n"
    msg += f"🔥 *Vice-Captain:* {team['vice_captain']}\n\n"
    msg += "_Expert Tips: Trust experience, pitch favors spin!_\n"
    return msg

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    message_text = data['message']['text']
    chat_id = data['message']['chat']['id']
    
    if "/team" in message_text.lower():
        match = get_today_match()
        if not match:
            bot.sendMessage(chat_id=chat_id, text="❌ No upcoming match today.")
        else:
            team = generate_team(match)
            msg = format_team_message(team)
            bot.sendMessage(chat_id=chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)
    return "OK"

@app.route("/")
def index():
    return "DreamXpert11 Bot is Running!"

# Deployment trigger
if __name__ == "__main__":
    app.run()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
