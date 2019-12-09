from constants import *
from discord.ext import commands
import discord

class Admin(commands.Cog, name=strings['_cog']['admin']):
    def __init__(self, bot):
        self.bot = bot
        self.color = maroon

    def cog_check(self, ctx):
        return ctx.message.author.guild_permissions.administrator

    async def cog_command_error(self, ctx, error):
        if type(error) == discord.ext.commands.errors.CheckFailure:
            await ctx.send(strings['not_admin'])

    @commands.command(aliases=['post'])
    async def embed(self, ctx, *args):
        """Send custom embed to a channel"""
        target_channel = ctx.message.channel_mentions[0] if ctx.message.channel_mentions else ctx.channel
        embed = discord.Embed(
            color=red,
            title=strings['embed_default_title'],
            description=strings['embed_default_description'] )
        inline = False
        (flags, flag_args) = pop_flags(args)
        for i, flag in enumerate(flags):
            value = flag_args[i]
            if flag in strings['embed_title']:
                embed.title = value
            elif flag in strings['embed_description']:
                embed.description = value
            elif flag in strings['embed_inline']:
                inline = 'y' in flag
            else:
                embed.add_field(name=flag.replace('_', ' '), value=value, inline=inline)

        return await target_channel.send(embed=embed)
    
    @commands.command(aliases=['role'])
    async def autorole(self, ctx, *args):
        """Grant roles to member on emoji add"""
        (flags, flag_args) = pop_flags(args)
        try:
            roles_input = flag_args[flags.index('roles')]
            role_map = string_to_dict(roles_input)
            if len(role_map) < 1:
                raise ValueError()
        except ValueError as e:
            return await ctx.send(strings['autorole_no_roles']) 

        message = await self.embed.callback(self, ctx, *tuple(args))

        reactions = role_map.keys()
        roles = role_map.values()
        for reaction in reactions:
            emoji = get_emoji_name(reaction)
            try:
                await message.add_reaction(get_emoji_object(emoji, ctx.guild))
            except discord.errors.HTTPException as e:
                print('bad emoji')
            data = dict( id=message.id, reactions=list_to_string(reactions), roles=list_to_string(roles) )
            autorole_db.upsert(data, ['id'])

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        id = reaction.message.id
        query = autorole_db.find_one(id=id)
        if user.bot or not query:
            return
        reactions = string_to_list(query['reactions'])
        roles = string_to_list(query['roles'])
        if (query):
            emoji = get_emoji_name(reaction)

            if emoji in reactions:
                index = reactions.index(emoji)
                role_name = roles[index]
                role = await get_role(user.guild, role_name)
                await user.add_roles(role)
            else:
                await reaction.remove(user)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        id = reaction.message.id
        query = autorole_db.find_one(id=id)
        if user.bot or not query:
            return
        reactions = string_to_list(query['reactions'])
        roles = string_to_list(query['roles'])
        if (query):
            emoji = get_emoji_name(reaction)
            if (emoji in reactions):
                index = reactions.index(emoji)
                role_name = roles[index]
                role = await get_role(user.guild, role_name)
                if (role in user.roles):
                    await user.remove_roles(role)

async def get_role(guild, name):
    """Get existing role and create it if it doesn't exist yet"""
    existing_role = discord.utils.get(guild.roles, name=name)
    return existing_role if existing_role else await guild.create_role(name=name)

def get_emoji_name(emoji):
    if emoji is discord.Emoji or emoji is discord.PartialEmoji:
        return emoji.name
    else:
        return str(emoji)

def get_emoji_object(emoji, guild):
    emoji_name = re.search('(?<=:).*(?=:)', emoji)
    if (emoji_name):
        emoji_name.group()
    custom_emoji = discord.utils.get(guild.emojis, name=emoji_name) 
    return custom_emoji if custom_emoji else emoji


def setup(bot):
    bot.add_cog(Admin(bot))