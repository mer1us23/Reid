# bot.py

# IMPORTS
import random
import discord
import os
from discord.ext import commands, tasks
import DiscordUtils
from discord.ext.commands.core import Command
from discord.ext.commands.errors import MissingPermissions
from dotenv import load_dotenv
from quotes import quotes
from discord.ext.commands import MissingPermissions
import asyncio

# LOAD PERMISSIONS
# intents = discord.Intents.default()
# intents.members = True

# LOAD THE TOKEN
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# CONNECT DISCORD BOT, SET PREFIX COMMAND AND BOT STATUS
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=""))
    print(f'{bot.user.name} has connected to Discord!')
    asyncio.create_task(sendQuote())   

# COMMAND DO NOT EXIST ERROR
# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.send('Bro, that command don\'t even exist!')


# CLEAR MESSAGES COMMAND
# @commands.has_permissions(manage_messages=True)
# @bot.command(name='clear', help='Clears the chat, you can specify how many messages to be deleted.')
# async def clearChat(ctx, amount=5):
#     if amount > 0:
#         await ctx.channel.purge(limit=amount + 1)
#         await ctx.send('The chat was deleted by a person with Manage Message Permission.')
#     elif amount <= 0:
#         await ctx.send('Please enter a value greater than 0')  

# @clearChat.error
# async def clearChat_error(ctx, error):
#     if isinstance(error, MissingPermissions):
#         await ctx.send('Bro, you can\'t do that!')

# SENDS MESSAGES EVERYDAY
# @tasks.loop(hours=24) 
# async def sendmessage():
#     users = [354329589515812865]
#     for id in users:
#         member = await bot.fetch_user(id)
#         try:
#             response = random.choice(quotes)
#             member.send(response)
#         except:
#             member.send("Don't worked!")

# # # MESSAGE REACTION
@tasks.loop(seconds=10)
async def sendQuote():
    user = await bot.fetch_user("354329589515812865")
    response = random.choice(quotes)
    await user.send(response)

sendQuote.start()
# GET THE DISCORD BOT RUNNING
bot.run(TOKEN)