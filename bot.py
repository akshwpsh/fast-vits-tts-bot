import discord
from discord.ext import commands
import json

with open('bot_config.json') as f:
    config = json.load(f)

Token = config['Token']
Prefix = config['Prefix']

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=Prefix, intents=intents)

@bot.event
async def on_ready():
    await bot.load_extension("bot_cog")
    print("Bot is ready")

bot.run(Token)