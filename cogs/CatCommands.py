from discord.ext import commands
import datetime
import aiohttp
import discord
import os
import random
import glob
CAT_DIR = os.getenv('CAT_DIR')


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
        #need cat api

    @commands.command(name='stats')
    async def on_stats(self, playername, ctx):
        """Get stats from PLP"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://plstats.plplatoon.com/?p={playername}') as r:
                if r.status == 200:
                    js = await r.json()
                    d = js[0]
                    embed = discord.Embed(title=f"Latest PL server stats for {playername}", color=0x0a0eff)
                    embed.add_field(name='Kills', value=str(d['Kills']), inline=True)
                    embed.add_field(name="Deaths", value=str(d['Deaths']), inline=True)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Something went wrong")



    @commands.command(name='status')
    async def on_status_request(self, ctx):
        """Gets status of the MC server"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.mcsrvstat.us/2/93.135.169.27') as r:
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

        #add your own here

        await message.channel.send(embed=embed)



def setup(bot):
    bot.add_cog(CatCommands(bot))
