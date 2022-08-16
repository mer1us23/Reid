# bot.py

# IMPORTS
import random
import discord
import os
from discord.ext import commands
import DiscordUtils
from discord.ext.commands.core import Command
from discord.ext.commands.errors import MissingPermissions
from dotenv import load_dotenv
from discordTogether import DiscordTogether
from quotes import quotes
from encouragements import encouragements
from discord.ext.commands import MissingPermissions

# LOAD PERMISSIONS
# intents = discord.Intents.default()
# intents.members = True

# LOAD THE TOKEN
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# CONNECT DISCORD BOT, SET PREFIX COMMAND AND BOT STATUS
music = DiscordUtils.Music()
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='bro ', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="u like a good bro <3"))
    print(f'{bot.user.name} has connected to Discord!')



# COIN FLIP COMMAND
@bot.command(name='flip', help='Play coin flip challenge')
async def flipFunction(ctx):
        coin = [
            '*Heads*',
            '*Tails*'
        ]
        response = random.choice(coin)
        await ctx.send(response)



# COMMAND DO NOT EXIST ERROR
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Bro, that command don\'t even exist!')


# CLEAR MESSAGES COMMAND
@commands.has_permissions(manage_messages=True)
@bot.command(name='clear', help='Clears the chat, you can specify how many messages to be deleted.')
async def clearChat(ctx, amount=5):
    if amount > 0:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send('The chat was deleted by a person with Manage Message Permission.')
    elif amount <= 0:
        await ctx.send('Please enter a value greater than 0')  

@clearChat.error
async def clearChat_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('Bro, you can\'t do that!')

# GET THE DISCORD BOT RUNNING
bot.run(TOKEN)
