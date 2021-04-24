# bot.py
# bot created by Francesco L.C. in association with nkaaf

import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
client = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

#client.load_extension("cogs.MusicCommands")
client.load_extension("cogs.CatCommands")
client.load_extension("cogs.AdminCommands")
client.load_extension("cogs.socials")
client.load_extension("cogs.webhooks")
def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()


