# bot.py
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.
bot = commands.Bot(command_prefix='!', intents=intents)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=intents)
#channel = client.get_channel(769940971038310422)
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if 'givecat' in message.content:
        await message.channel.send(file=discord.File(r"/home/DiscordBot/catpics/" + (random.choice(os.listdir(r"/home/DiscordBot/catpics/")))))
    if 'this bot sucks' in message.content:
        await message.channel.send(f'{message.author.mention} sucks')
    if 'tell a joke' in message.content:
        await message.channel.send('<@209748800057638914>')
    if 'pet cat' in message.content:
        await message.channel.send('''purrr... the cat liked it''')

#@client.event
#class CustomClient(discord.Client):
#    async def on_ready(self):
#        #guild = discord.utils.get(client.guilds, name=GUILD)
#        print(
#            f'{self.user} has connected to Discord!'
            #f'{client.user} is connected to the following guild:\n'
            #f'{guild.name}(id: {guild.id})'
#        )
        #members = '\n - ' .join([member.name for member in guild.members])
        #print(f'Guild Members:\n - {members}')

#client = CustomClient()
client.run(TOKEN)