print('''
 _____         _               
|     |___ ___| |_ ___ _ _ ___ 
|  |  |  _| . |   | -_| | |_ -|
|_____|_| |  _|_|_|___|___|___|
          |_| Hack Club Dinosaur 
''')

import discord
import pytz
from os import listdir
from os.path import isfile, join
from discord.ext import commands
from constants import *

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
    print('{} is online!'.format(bot.user.name))

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
        await ctx.send(strings['fatal_error'])

# add cogs (groups of commands)
cogs_path = './cogs'
cog_file_names = [f[:f.index('.')] for f in listdir(cogs_path) if isfile(join(cogs_path, f))]
for cog_name in cog_file_names:
    bot.load_extension('cogs.' + cog_name)
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