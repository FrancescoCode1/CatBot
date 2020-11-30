from discord.ext import commands
import datetime
import aiohttp
import discord
import os
import random
import glob
CAT_DIR = os.getenv('CAT_DIRlin')


class CatCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='givecat')
    async def on_givecat(self, ctx):
        """Sends a random cat picture to the channel"""
        await ctx.send(file=discord.File(random.choice(glob.glob(CAT_DIR + '/*'))))


    @commands.command(name='this bot sucks')
    async def on_bot_insult(self, ctx):
        await ctx.send(f'{ctx.author.mention} sucks')


    @commands.command(name='pet_cat')
    async def on_pet_cat(self, ctx):
        """Come on, you have to"""
        await ctx.send('''purrr... the cat liked it''')


    @commands.command(name='status')
    async def on_status_request(self, ctx):
        """Gets status of the MC server"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.mcsrvstat.us/2/62.104.69.117') as r:
                if r.status == 200:
                    js = await r.json()
                    if js['online']:
                        color = 0x008000
                    else:
                        color = 0xFF0000
                    embed = discord.Embed(title='Server Stats', description=js['ip'], color=color)
                    embed.add_field(name='Server Up?', value=str(js['online']))
                    if js['online']:
                        embed.add_field(name='Players online',
                                        value=str(js['players']['online']) + '/' + str(js['players']['max']))
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("This aint supposed to happen")

    @commands.command(name='setembed')
    @commands.is_owner()
    async def on_setembed(self, message):

        """placeholder, add your embed here if you want one"""



def setup(bot):
    bot.add_cog(CatCommands(bot))
