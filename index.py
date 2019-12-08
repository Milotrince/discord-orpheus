print('''
 _____         _               
|     |___ ___| |_ ___ _ _ ___ 
|  |  |  _| . |   | -_| | |_ -|
|_____|_| |  _|_|_|___|___|___|
          |_| Hack Club Dinosaur 
''')

import discord
import pytz
import dataset
from random import choice
from datetime import datetime, timedelta
from discord.ext import commands
from constants import *

def log(content):
    print('{} {}'.format(datetime.now(), content))

def determine_prefix(bot, message):
    prefixes = strings['prefixes']
    prefixes.append(bot.user.mention + ' ')
    return prefixes

# Define bot
bot = commands.Bot(
    command_prefix=determine_prefix, 
    case_insensitive=True,
    activity=discord.Game(strings['bot_presence']))
bot.remove_command('help')

@bot.event
async def on_ready():
    print('{0.user} is online!'.format(bot.user.name))

@bot.event
async def on_disconnect():
    print('{} has disconnected...'.format(bot.user.name))

# Disable for full stack trace
@bot.event
async def on_command_error(ctx, error):
    """Sends a message when command error is encountered."""
    if type(error) == commands.errors.CommandNotFound:
        await ctx.send(strings['invalid_command'])
    else:
        log("===== ERROR RAISED FROM: " + ctx.message.content)
        print(error)

# add cogs (groups of commands)
cogs_folder = 'cogs'
cogs = [ 'generic', 'club', 'fun' ]
for cog_name in cogs:
    bot.load_extension(cogs_folder + '.' + cog_name)
for cog in bot.cogs.values():
    for command in cog.get_commands():
        # Use only if want override from strings.json
        # command.aliases = strings['_aliases'][command.name]
        # command.help = '\n'.join(strings['_help'][command.name])
        # command.name = strings['_name'][command.name]
        pass

# Run bot
authfile = open('.auth', 'r')
bot.run(authfile.read())