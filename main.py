import os
import discord
from discord.ext import commands

token = os.environ.get('TOKEN')

intents = discord.Intents.default()
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

if not token:
    raise ValueError("TOKEN non definito")
bot.run(token)
