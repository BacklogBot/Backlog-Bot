# bot.py
import os

import discord
import random
from game import Game
from backlog import Backlog

# import interactions
# from interactions import Client, Message #pip install discord-interactions.py
# from interactions.ext.wait_for import wait_for, setup
import asyncio

from dotenv import load_dotenv
from discord.ext import commands

backlogs = dict([])

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='/', intents = discord.Intents.all())

backlogs = dict() #dictionary which uses the member name as a key and the backglog as a value

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, I see you are a new user.'
    )

# @bot.event
# async def on_message(message): 
#     if message.author == bot.user: #this is to prevent the bot from responding to itself
#         return

#     print(f'message: {message.content}')
#     if message.content == '99!':
#         response = random.choice(brooklyn_99_quotes)
#         await message.channel.send(response)
#     elif message.content == 'raise-exception':
#         raise discord.DiscordException

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

#COMMANDS-------------------------------------------------------------------------------------------------- 

@bot.command(pass_context=True, name='helpBacklog') #needed to change name because help was already taken
async def helpBacklog(ctx, *args):
    return await ctx.send("/helpBacklog not implemented")

@bot.command(pass_context=True, name='newBacklog')
async def newBacklog(ctx, *args):
    username = ctx.message.author.name #retrieve the user name of whoever issued the commmand

    #check to see if the user already has a backlog
    if username in backlogs:
        return await ctx.send('You already have an existing backlog.') 

    #check function for the list of prefered genres 
    def checkGenre(msg): 
        if(int(msg.author.id) == int(ctx.author.id)): #verify that it is the same user
            return True
        return False

    #check function for the average playtime 
    def checkTime(msg): 
        if(int(msg.author.id) == int(ctx.author.id)): #verify that it is the same user 
            if(msg.content.isdigit()):
                return True
            else:
                return False
        else:
            return False

    #prompt the user for their list of prefered genres
    await ctx.send("Please enter a list of your prefered genres.")
    try:
        msg1 = await bot.wait_for("message", check=checkGenre, timeout= 5 * 60) #timeout 5 min
    except asyncio.TimeoutError:
        return await ctx.send('{} request timeout....'.format(username)) 

    #prompt the user for average amount of available playtime in a day
    await ctx.send("Please enter a enter your average amount of available playtime.")
    try:
        msg2 = await bot.wait_for("message", check=checkTime, timeout= 5 * 60) #timeout 5 min
    except asyncio.TimeoutError:
        return await ctx.send('{} request timeout....'.format(username))

    #add the backlog to the backglogs dictionary
    genres =  set(msg1.content.split())
    avgTime = int(msg2.content)
    backlogs[username] = Backlog(username, genres, avgTime)

    #confirm backlog creation 
    return await ctx.send("{}'s backlog created!".format(username))

@bot.command(pass_context=True, name='addGame')
async def addGame(ctx, *args):
    username = ctx.message.author.name #retrieve the user name of whoever issued the commmand 

    if username not in backlogs:
        return await ctx.send('I am sorry {}, it seems that you have not yet created a backlog, if you would \
                            to do so, simply type "/newBacklog in the chat. For further help type /help to get \
                            a list of possible commands, or for a specific command type /help followed by said \
                            command.'.format(username))

    #check functions (will need further modification for error checking)

    def checkStr(msg): #basic check function, just ensures that the users are the same
        if(int(msg.author.id) == int(ctx.author.id)): #verify that it is the same user
            return True
        return False

    #check function for the average playtime 
    def checkDigit(msg): #check function, ensure that the reply is a number 
        if(int(msg.author.id) == int(ctx.author.id)): #verify that it is the same user 
            if(msg.content.isdigit()): #verify that the msg is a number
                return True
            else:
                return False
        else:
            return False

    #prompt the user for the game's name
    await ctx.send("Please enter the game's name.")
    try:
        msg1 = await bot.wait_for("message", check=checkStr, timeout= 5 * 60) #timeout 5 min
    except asyncio.TimeoutError:
        return await ctx.send('{} request timeout....'.format(username)) 

    #prompt the user for the the game's genres
    await ctx.send("Please enter the game's genres seperated by spaces.")
    try:
        msg2 = await bot.wait_for("message", check=checkStr, timeout= 5 * 60) #timeout 5 min
    except asyncio.TimeoutError:
        return await ctx.send('{} request timeout....'.format(username)) 

    #prompt the user for the estimated time of the game 
    await ctx.send("Please enter how long the games take on average in hours.")
    try:
        msg3 = await bot.wait_for("message", check=checkDigit, timeout= 5 * 60) #timeout 5 min
    except asyncio.TimeoutError:
        return await ctx.send('{} request timeout....'.format(username)) 

    #prompt the user for the amount of time played
    await ctx.send("Please enter how long you have already played this game in hours, entering 0 if you have yet to play it.")
    try:
        msg4 = await bot.wait_for("message", check=checkDigit, timeout= 5 * 60) #timeout 5 min
    except asyncio.TimeoutError:
        return await ctx.send('{} request timeout....'.format(username)) 

    #prompt the user for the their current interest in the game 
    await ctx.send("Please enter your current interest in the game, out of 10.")
    try:
        msg5 = await bot.wait_for("message", check=checkDigit, timeout= 5 * 60) #timeout 5 min
    except asyncio.TimeoutError:
        return await ctx.send('{} request timeout....'.format(username)) 

    name = msg1.content
    genres = set(msg2.content.split())
    avgTime = int(msg3.content)
    timePlayed = int(msg4.content)
    interest = int(msg5.content)

    backlogs[username].addGame(Game(name, interest, avgTime, genres, timePlayed))

@bot.command(name='delGame')
async def delGame(ctx, name):
    username = ctx.message.author.name 

    if(backlogs[username].delGame(name)): #if backlog could not find said game to remove
        return await ctx.send("{} was not found in your backlog, {}".format(name, username))
    else:
        return await ctx.send("{} was removed from your backlog, {}".format(name, username))

@bot.command(name='list')
async def list(ctx, *args):
    #list games in alphabetical order instead of via score 

    return await ctx.send("/list not implemented.")

@bot.command(name='suggestGames')
async def suggestGames(ctx, *args):
    #list games in order of their scores, higher scores first 
    username = ctx.message.author.name 

    if username not in backlogs: #tempeory implementation with no arguments 
        await ctx.send("You have yet to create a backlog, {}".format(username))
    else:
        print(backlogs[username])
        return await ctx.send(str(backlogs[username]))

@bot.command(name='edit')
async def edit(ctx, *args):   
    return await ctx.send("/edit not implemented.")

@bot.command(name='fq')
async def fq(ctx, *args):
    return await ctx.send("/fq not implemented.")
    await ctx.send(response)

bot.run(TOKEN)