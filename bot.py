# bot.py

# IMPORTS
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

# SENDS MESSAGES EVERYDAY
@tasks.loop(hours=12)
async def sendQuote():
    user = await bot.fetch_user("354329589515812865")
    response = random.choice(quotes)
    await user.send(response)

@bot.event
async def on_ready():
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=""))
    print(f'{bot.user.name} has connected to Discord!')
    user = await bot.fetch_user("354329589515812865")
    await user.send("salut, eu sunt bot-ul tau de citate din carti. daca doresti sa incepem, scrie !start in chat.")
    

# COMMAND DO NOT EXIST ERROR
# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.send('Bro, that command don\'t even exist!')


@bot.command(name="start")
async def _command(ctx):
    await ctx.send(f"te rog alege din lista de la ce carte doresti sa-ti trimit citate.\n1. Arta subtila a nepasarii. O metoda nonconformista pentru o viata mai buna - Mark Manson\n2. Fuck! De ce nu mă schimb? - Dr. Gabija Toleikyte")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
        msg.content.lower() in ["1", "2"]
    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        if msg.content.lower() == "1":
            await ctx.send("ai ales cartea: Arta subtila a nepasarii. O metoda nonconformista pentru o viata mai buna - Mark Manson\nvei primi un citat random in fiecare zi la 12 ore incepand de acum!\ndaca vrei sa opresti procesul, atunci scrie !stop.")
            await sendQuote.start()
        elif msg.content.lower() == "2":
            await ctx.send("Ai ales cartea: Fuck! De ce nu mă schimb? - Dr. Gabija Toleikyte (deocamdata este in lucru)")
    except asyncio.TimeoutError:
        await ctx.send("scuze, dar nu ai raspuns in 30 de secunde! foloseste iar !start.")


@bot.command(name="stop")
async def _command(ctx):
    await ctx.send("ai ales sa opresti bot-ul din a mai trimite citate din carte. daca doresti sa incepi iar, tasteaza !start.")
    try:
        sendQuote.stop()
    except:
        await ctx.send("nu i-ai spus bot-ului din ce carti sa-ti trimita citate.")
# GET THE DISCORD BOT RUNNING
bot.run(TOKEN)