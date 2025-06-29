import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)

@app.route('/alive')
def alive():
    return "I'm alive!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

def start_keep_alive():
    thread = Thread(target=run_flask)
    thread.daemon = True
    thread.start()

    def ping():
        try:
            r = requests.get("http://127.0.0.1:10000/alive")
            print(f"✅ Ping: {r.status_code}")
        except Exception as e:
            print(f"❌ Ping fallito: {e}")

    scheduler = BackgroundScheduler()
    scheduler.add_job(ping, "interval", seconds=600)
    scheduler.start()

start_keep_alive()

token = os.environ.get("TOKEN")
if not token:
    raise ValueError("TOKEN non definito")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

@bot.tree.command(name="ciao", description="Saluta il bot")
async def ciao(interaction: discord.Interaction):
    await interaction.response.send_message("Ciao anche a te!")

bot.run(token)
