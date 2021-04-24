import discord
from discord.ext import commands
import aiohttp

class webhooks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="git")
    async def on_git(self, ctx):
        async with aiohttp.ClientSession() as session:
            #async with session.get(f"https://api.github.com/repos/nginxinc/docker-nginx/commits") as r:
            async with session.get(f"https://api.github.com/repos/francescocode1/catbot/commits") as r:

                if r.status == 200:
                    js = await r.json()
                    d = js[0]
                    embed = discord.Embed(title=f"Letzter Commit in nginx/docker-nginx")
                    embed.add_field(name='Name:', value=str(d["commit"]["author"]["name"]) + "/" + str(d["author"]["login"]), inline=True)
                    embed.add_field(name='Zeit:', value=str(d["commit"]["author"]["date"]), inline=True)
                    embed.add_field(name='Message:', value=str(d["commit"]["message"]), inline=False)
                    await ctx.send(embed=embed)
                elif r.status == 404:
                    await ctx.send("Error status 404")
                elif r.status == 500:
                    await ctx.send("Error status 500")
                else:
                    await ctx.send("unknown error")

def setup(bot):
    bot.add_cog(webhooks(bot))
