# bot.py

# IMPORTS
import random
import discord
import os
from discord.ext import commands
import DiscordUtils
from discord.ext.commands.core import Command
import youtube_dl
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


# SEND DM TO NEW MEMBERS
@bot.event
async def on_member_join(member):
    await member.send(
        f'Hi {member.name}, welcome to my server!'
    )

# ENCOURAGEMENTS MESSAGES
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'sad':
        response = random.choice(encouragements)
        await message.channel.send(response)
    await bot.process_commands(message)

# QUOTE COMMAND
@bot.command(name='quote', help='Shows a random quote')
async def quoteFunction(ctx):
    response = random.choice(quotes)
    await ctx.send(response)

# LIST COMMAND
@bot.command(name='list', help='Shows a list with words where the bot can respond')
async def quoteFunction(ctx):
    await ctx.send('> sad')

# COIN FLIP COMMAND
@bot.command(name='flip', help='Play coin flip challenge')
async def flipFunction(ctx):
        coin = [
            '*Heads*',
            '*Tails*'
        ]
        response = random.choice(coin)
        await ctx.send(response)

# ROLLING DICE COMMAND
@bot.command(name='rolldice', help='Play roll dice challenge')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

# DISCORD TOGETHER
togetherControl = DiscordTogether(bot)

# YOUTUBE COMMAND
@bot.command(name='ytb', help='Watch YouTube at the same time with your friends')
async def startYT(ctx):
    if ctx.author.voice == None:
        return await ctx.send('Please join a voice channel.')
    link = await togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
    await ctx.send(f"Bro, click the blue link!\n{link}")
    
# POKER COMMAND
@bot.command(name='poker', help='Play Poker with your friends or bots')
async def startPoker(ctx):
    if ctx.author.voice == None:
        return await ctx.send('Please join a voice channel.')
    link = await togetherControl.create_link(ctx.author.voice.channel.id, 'poker')
    await ctx.send(f"Bro, click the blue link!\n{link}")

# CHESS COMMAND
@bot.command(name='chess', help='Play Chess with your friends')
async def startChess(ctx):
    if ctx.author.voice == None:
        return await ctx.send('Please join a voice channel.')
    link = await togetherControl.create_link(ctx.author.voice.channel.id, 'chess')
    await ctx.send(f"Bro, click the blue link!\n{link}")
    
# COMMAND ROLLDICE ERROR // for all commands bot.event
@roll.error
async def roll_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You need to specify the number of dice and number of slides.')

# COMMAND DO NOT EXIST ERROR
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Bro, that command don\'t even exist!')

# YOUTUBE MUSIC COMMAND NEW

# @bot.command(name='join', help='Join a voice channel.')
# async def join(ctx):
#     voicetrue = ctx.author.voice
#     mevoicetrue = ctx.guild.me.voice
#     if voicetrue is None:
#         return await ctx.send('You are not in a voice channel!')
#     if not mevoicetrue is None:
#         return await ctx.send('I am already in voice channel!')
#     await ctx.author.voice.channel.connect()
#     await ctx.send('The bot joined your voice channel!')


@bot.command(name='leave', help='Leave a voice channel.')
async def leave(ctx):
    voicetrue = ctx.author.voice
    mevoicetrue = ctx.guild.me.voice
    if voicetrue is None:
        return await ctx.send('You are not in a voice channel!')
    if mevoicetrue is None:
        return await ctx.send('I am not in a voice channel!')
    player = music.get_player(guild_id=ctx.guild.id)
    await player.stop()
    await ctx.voice_client.disconnect()
    await ctx.send('The bot left your voice channel!')


@bot.command(name='play', help='Play a song from YouTube.')
async def play(ctx, *, url):
    mevoicetrue = ctx.guild.me.voice
    voicetrue = ctx.author.voice
    if voicetrue is None:
        return await ctx.send('You are not in a voice channel!')
    if mevoicetrue is None:
        await ctx.author.voice.channel.connect()
    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        await player.queue(url, search=True)
        song = await player.play()
        await ctx.send(f"Playing {song.name}")
    else:
        song = await player.queue(url, search=True)
        await ctx.send(f"Queued {song.name}")


@bot.command(name='pause', help='Pause the current song playing.')
async def pause(ctx):
    voicetrue = ctx.author.voice
    mevoicetrue = ctx.guild.me.voice
    if voicetrue is None:
        return await ctx.send('You are not in a voice channel!')
    if mevoicetrue is None:
        return await ctx.send('I am not in a voice channel!')
    if not ctx.voice_client.is_playing():
        await ctx.send("No song is playing, bro.")
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    await ctx.send(f"Paused {song.name}")
        


@bot.command(name='resume', help='Resume the current song playing.')
async def resume(ctx):
    voicetrue = ctx.author.voice
    mevoicetrue = ctx.guild.me.voice
    if voicetrue is None:
        return await ctx.send('You are not in a voice channel!')
    if mevoicetrue is None:
        return await ctx.send('I am not in a voice channel!')
    if not ctx.voice_client.is_playing():
        await ctx.send("No song is playing, bro.")
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    await ctx.send(f"Resumed {song.name}")


@bot.command(name='stop', help='Stop the current song playing.')
async def stop(ctx):
    voicetrue = ctx.author.voice
    mevoicetrue = ctx.guild.me.voice
    if voicetrue is None:
        return await ctx.send('You are not in a voice channel!')
    if mevoicetrue is None:
        return await ctx.send('I am not in a voice channel!')
    if not ctx.voice_client.is_playing():
        await ctx.send("No song is playing, bro.")
    player = music.get_player(guild_id=ctx.guild.id)
    await player.stop()
    await ctx.send("Stopped")

@bot.command(name='loop', help='Loop the current song playing.')
async def loop(ctx):
    voicetrue = ctx.author.voice
    mevoicetrue = ctx.guild.me.voice
    if voicetrue is None:
        return await ctx.send('You are not in a voice channel!')
    if mevoicetrue is None:
        return await ctx.send('I am not in a voice channel!')
    if not ctx.voice_client.is_playing():
        await ctx.send("No song is playing, bro.")
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        await ctx.send(f"Enabled loop for {song.name}")
    else:
        await ctx.send(f"Disabled loop for {song.name}")

@bot.command(name='np', help='Shows song name.')
async def np(ctx):
    voicetrue = ctx.author.voice
    mevoicetrue = ctx.guild.me.voice
    if voicetrue is None:
        return await ctx.send('You are not in a voice channel!')
    if mevoicetrue is None:
        return await ctx.send('I am not in a voice channel!')
    if not ctx.voice_client.is_playing():
        await ctx.send("No song is playing, bro.")
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    await ctx.send(f"Now playing {song.name}")


@bot.command(name='skip', help='Skip the song playing.')
async def skip(ctx):
    voicetrue = ctx.author.voice
    mevoicetrue = ctx.guild.me.voice
    if voicetrue is None:
        return await ctx.send('You are not in a voice channel!')
    if mevoicetrue is None:
        return await ctx.send('I am not in a voice channel!')
    if not ctx.voice_client.is_playing():
        await ctx.send("No song is playing, bro.")
    player = music.get_player(guild_id=ctx.guild.id)
    data = await player.skip(force=True)
    if len(data) == 2:
        await ctx.send(f"Skipped {data[0].name}")
    else:
        await ctx.send(f"Skipped {data[0].name}")
    temp = bot.get_command(name='np')
    await temp.callback(ctx)
        

# @bot.event
# async def on_voice_state_update(member, prev, cur):
#     if bot.user in prev.channel.members and len([m for m in prev.channel.members if not m.bot]) == 0:
#         channel = discord.utils.get(bot.voice_clients, channel=prev.channel)
#         await channel.disconnect()

@bot.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None:
        # Exiting if the bot it's not connected to a voice channel
        return

    if len(voice_state.channel.members) == 1:
        await voice_state.disconnect()
        await member.send("I'm out too bro!")
  
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
