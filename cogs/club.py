from constants import *
from discord.ext import commands
import discord

class Club(commands.Cog, name=strings['_cog']['club']):
    def __init__(self, bot):
        self.bot = bot
        self.color = red

    @commands.command(aliases=['links', 'github'])
    async def resources(self, ctx):
        """Show links of clubstuff and more"""
        embed=discord.Embed(
            title='Resources',
            color=red,
            description=(strings['resources'])
        )
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Club(bot))