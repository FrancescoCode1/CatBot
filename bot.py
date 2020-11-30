# bot.py
# bot created by Francesco L.C. in association with nkaaf
# ver 0.5 milestone release
import discord
import os
'''This simply starts the bot. Token is saved in the .env.'''

from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
client = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

client.load_extension("cogs.MusicCommands")
client.load_extension("cogs.CatCommands")
client.run(TOKEN)
