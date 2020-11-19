# bot.py
# bot created by Francesco L.C. in association with nkaaf
import os                               #Cogs allows me to actually keep the main bot tidy
import discord                          #Im only importing libs needed to run the bot. Inside cogs all the libs are loaded

from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()     #Subs to intent
client = commands.Bot(command_prefix='!', intents=intents)  #cmd prefix is set

load_dotenv()                           #.env file containing token is loaded

TOKEN = os.getenv('DISCORD_TOKEN')      #Token string is given to TOKEN variable

client.load_extension("cogs.MusicCommands") #juicy part. cogs are loaded into the bot
client.load_extension("cogs.CatCommands")   #more functionalities require more code. with cogs you keep the overview

client.run(TOKEN)                           #token is used to authenticate the bot and actually run it
