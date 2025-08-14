# -------------------
# Keep-alive web server
# -------------------
from flask import Flask
import threading

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

# Start the web server in a separate thread so it doesn't block the bot
threading.Thread(target=run).start()


# -------------------
# Discord Bot
# -------------------
import discord
from discord.ext import tasks
import os
import datetime

TOKEN = os.getenv("DISCORD_TOKEN")
VIP_CHANNEL_ID = int(os.getenv("VIP_CHANNEL_ID"))
FREE_CHANNEL_ID = int(os.getenv("FREE_CHANNEL_ID"))
VIP_ROLE_ID = int(os.getenv("VIP_ROLE_ID"))

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

def get_best_tips():
    # Placeholder – replace with real API logic later
    return [
        "✅ Team A to win vs Team B",
        "⚠️ Over 2.5 goals in Match X",
        "✅ Draw no bet: Team C"
    ]

@tasks.loop(hours=24)
async def post_free_tip():
    channel = bot.get_channel(FREE_CHANNEL_ID)
    tip = get_best_tips()[0]  # just first tip for free
    await channel.send(f"**Free Tip {datetime.date.today()}**\n{tip}")

@tasks.loop(hours=8)
async def post_vip_tips():
    channel = bot.get_channel(VIP_CHANNEL_ID)
    tips = "\n".join(get_best_tips())
    mention = f"<@&{VIP_ROLE_ID}>"
    await channel.send(f"{mention} **VIP Tips {datetime.date.today()}**\n{tips}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    post_free_tip.start()
    post_vip_tips.start()

bot.run(TOKEN)