# bot.py

# IMPORTS
import datetime as dt
import random
from tabnanny import check
import discord
import os
from discord.ext import commands, tasks
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
bot.remove_command('help')


# BOT ON READY AND ACTIVITY
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="a book"))
    print(f'{bot.user.name} has connected to Discord!')

# HELP COMMAND
@bot.command(name="help")
async def _command(ctx):
    await ctx.send("**LISTA CU COMENZI**\n!start -> pentru a incepe procesul de trimitere citat.\n!stop -> pentru a opri procesul de trimitere citat.\n!list -> pentru a vedea lista cu carti.")

# COMMAND DO NOT EXIST ERROR
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('comanda nu exista, tasteaza !help pentru a vedea comenzile.')

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
#     global id 
#     id = message.author.id
#     await bot.process_commands(message)

# START COMMAND
@bot.command(name="start")
async def _command(ctx):
    await ctx.send(f"te rog alege din lista de la ce carte doresti sa-ti trimit citate.\n1. Arta subtila a nepasarii. O metoda nonconformista pentru o viata mai buna - Mark Manson\n2. Fuck! De ce nu mă schimb? - Dr. Gabija Toleikyte")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
        msg.content.lower() in ["1", "2"]
    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        if msg.content.lower() == "1":
            await ctx.send("ai ales cartea: Arta subtila a nepasarii. O metoda nonconformista pentru o viata mai buna - Mark Manson\nvei primi un citat random in fiecare zi incepand de acum!\ndaca vrei sa opresti procesul, atunci scrie !stop.")
            await sendQuote.start()
        elif msg.content.lower() == "2":
            await ctx.send("Ai ales cartea: Fuck! De ce nu mă schimb? - Dr. Gabija Toleikyte (deocamdata este in lucru)")
    except asyncio.TimeoutError:
        await ctx.send("scuze, dar nu ai raspuns in 30 de secunde! foloseste iar !start.")

# SENDS MESSAGES EVERYDAY
@tasks.loop(hours=11, reconnect=True)
async def sendQuote():
    user = await bot.fetch_user("354329589515812865")
    response = random.choice(quotes)
    await user.send(response)

# STOP COMMAND
@bot.command(name="stop")
async def _command(ctx):
    await ctx.send("ai ales sa opresti bot-ul din a mai trimite citate din carte. daca doresti sa incepi iar, tasteaza !start.")
    try:
        sendQuote.stop()
    except:
        await ctx.send("nu i-ai spus bot-ului din ce carti sa-ti trimita citate.")


# LIST COMMAND
@bot.command(name="list")
async def _command(ctx):
    await ctx.send("**LISTA CU CARTI**\n1. Arta subtila a nepasarii. O metoda nonconformista pentru o viata mai buna - Mark Manson\n2. Fuck! De ce nu mă schimb? - Dr. Gabija Toleikyte (deocamdata este in lucru)")

# # WORKS COMMAND
# @bot.command(name="works")
# async def _command(ctx):
#     if sendQuote.is_running() is False:
#         await ctx.send("I am not running anything!")
#         print(sendQuote.is_running())
#     else:
#         await ctx.send("I am running your quote!")
#         print(sendQuote.is_running())

# @bot.command(name="failed")
# async def _command(ctx):
#     if sendQuote.failed() == "True":
#         print("The bot has failed the quote!")
#     else:
#         print("Everything is fine!")

# @bot.command(name="restart")
# async def _command(ctx):
#     sendQuote.restart()

# @tasks.loop(hours=1)
# async def verify():
#     print("Is the process still running?", sendQuote.is_running())
#     print("Had the process failed?", sendQuote.failed())
    
# verify.start()

# GET THE DISCORD BOT RUNNING
try:    
    bot.run(TOKEN)
except:
    os.system("kill 1")

