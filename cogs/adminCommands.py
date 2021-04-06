import discord
from discord.ext import commands
import time

class adminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def userkick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f"User {member} has been kicked!")
        except:
            await ctx.send("Something went wrong. Check the logs!")

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def userban(self, ctx, member: discord.Member, *, reason=None):
        try:
            if reason == None:
                await ctx.send("Please provide a reason")
            else:
                await member.ban(reason=reason)
                await ctx.send(f"User {member} has been banned for {reason}!")
        except:
            await ctx.send("Something went wrong. Check the logs!")

    @commands.command(name="tempban")
    @commands.has_permissions(ban_members=True)
    async def usertban(self, ctx, member: discord.Member, *, duration=None, reason=None):
        try:
            if reason == None or duration == None:
                await ctx.send("Please provide ban duration or reason")
            else:
                await ctx.send(f"User {member} has been banned for {duration}")
                await member.ban(reason=reason)
                await time.sleep(duration * 60 * 60 * 24)
                await member.unban()
        except:
            await ctx.send("Something went wrong check the logs")

    def setup(bot):
        bot.add_cog(adminCommands(bot))
