from constants import *
from discord.ext import commands
import discord

class Fun(commands.Cog, name=strings['_cog']['fun']):
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.gold()

    @commands.command(aliases=['hello', 'dinosaur-noises'])
    async def hi(self, ctx):
        """Say hi!"""
        await ctx.send(strings['greeting'])

def setup(bot):
    bot.add_cog(Fun(bot))