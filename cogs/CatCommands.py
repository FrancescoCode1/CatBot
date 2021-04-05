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

        embed = discord.Embed(title="Willkommen auf dem APACHE HELICOPTER Discord", colour=discord.Colour(0x8f3b4d),
                                  description="Wir sind ein CS:GO und Minecraft Gaming Server mit :heart:",
                                  timestamp=datetime.datetime.utcfromtimestamp(1605357933))

        embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/730/header.jpg?t=1604621473")
        embed.set_thumbnail(url="https://images-eu.ssl-images-amazon.com/images/I/512dVKB22QL._AC_UL600_SR600,600_.png")
        embed.set_author(name="FD", url="https://discordapp.com",
                             icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.set_footer(text="FD", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

        embed.add_field(name="Rollen", value="Zurzeit gibt es nur die @APACHEN Rolle fÃ¼r Member", inline=False)
        embed.add_field(name="Zum Bot",
                            value="Der CatBot ist eine eigene Entwicklung und wird durchgehend mit Funktionen erweitert",
                            inline=False)
        embed.add_field(name="Links:",
                            value="[Steamgruppe](https://steamcommunity.com/groups/CodeAphe)\n[Neues Survival-Spiel von befreundeten Devs](https://store.steampowered.com/app/1090800/Northern_Lights/)")

        await message.channel.send(embed=embed)



def setup(bot):
    bot.add_cog(CatCommands(bot))