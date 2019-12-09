from constants import *
from discord.ext import commands
import discord

class Generic(commands.Cog, name=strings['_cog']['generic']):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.color = discord.Color.greyple()
        
    @commands.command(aliases=['pong'])
    async def ping(self, ctx):
        """Pong! Shows latency."""
        return await ctx.send(strings['ping'].format(round(self.bot.latency, 1)))

    @commands.command(aliases=['bio'])
    async def about(self, ctx):
        """
        All about me!
        """
        embed = discord.Embed(
            color=red,
            description=strings['about'] )
        embed.set_author(name="About Me")
        return await ctx.send(embed=embed)


    @commands.command(aliases=['commands', 'command'])
    async def help(self, ctx, *args):
        """
        Shows descriptions of all or specific commands.
        ...Like this. Pretty meta.
        """
        filtered_commands = []
        for arg in args:
            for c in self.bot.commands:
                if (c.name == arg or arg in c.aliases) and c not in filtered_commands:
                    filtered_commands.append(c)
        if len(filtered_commands) > 0:
            for command in filtered_commands:
                embed = discord.Embed(
                    color=self.bot.cogs[command.cog_name].color,
                    title=command.name )
                embed.add_field(
                    name="aka `{}`".format("`, `".join(command.aliases)),
                    value=command.help,
                    inline=False )
                await ctx.send(embed=embed)
            return

        for cog_name, cog in self.bot.cogs.items():
            has_access = cog.cog_check(ctx)
            if has_access:
                embed = discord.Embed(
                    color=cog.color,
                    title="{} {}".format(cog_name, strings['commands']) )
                for command in sorted(cog.get_commands(), key=lambda c:c.name):
                    embed.add_field(
                        name="**{}**    aka `{}`".format(command, "`, `".join(command.aliases)),
                        value=command.short_doc,
                        inline=False )
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Generic(bot))