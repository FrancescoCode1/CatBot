# bot.py
# bot created by Francesco L.C. in association with nkaaf
import os
import discord
import discord
from discord.ext import commands
import threading
import os
"""
from random import shuffle, choice
from cogs.utils.dataIO import dataIO
from cogs.utils import checks
from cogs.utils.chat_formatting import pagify, escape
from urllib.parse import urlparse
from __main__ import settings"""

from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
client = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

client.load_extension("cogs.MusicCommands")
client.load_extension("cogs.CatCommands")
#client.load_extension("cogs.musix")
client.run(TOKEN)


