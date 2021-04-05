import discord
from discord.ext import commands

class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban")
    @commands.has_role(item=int(782305240015437875))
    async def on_ban(self, member, ctx):

        

