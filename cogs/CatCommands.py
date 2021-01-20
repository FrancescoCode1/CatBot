from discord.ext import commands
import datetime
import aiohttp
import discord
import os
import random
import glob
CAT_DIR = os.getenv('CAT_DIRlin')
#Adding triple quotation marks below definition of a function creates description for the command in "!help" command

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
        
    @commands.command(name='stats')
    async def onStats(self, ctx, player):
        data = urllib.request.urlopen(f"http://plstats.plplatoon.com/?p={player}").read()
        output = json.loads(data)
        stats = output[0]
        embed = discord.Embed(title=f"Latest PL server stats for {player}", color=0x0a0eff)
        embed.add_field(name='Kills', value=str(stats['Kills']), inline=False)
        embed.add_field(name="Deaths", value=str(stats['Deaths']), inline=False)
        embed.add_field(name="Headshots", value=str(stats["Headshots"]), inline=False)
        embed.add_field(name="Killstreak", value=str(stats["Killstreak"]), inline=False)
        await ctx.send(embed=embed)

    #Basic MC server Checker, can be useful if you have an mc community server. might add autocheck to check in interval
    @commands.command(name='status')
    async def on_status_request(self, ctx):
        """Gets status of the MC server"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.mcsrvstat.us/2/insert-ip-here') as r:
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
