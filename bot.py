# bot.py
import os

import discord
import random
import game
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
    # username = ctx.message.author.name #retrieve the user name of whoever issued the commmand 

    # if username in backlogs:
    #     backlogs[username].append()
    # else:
    #     ctx.send('I am sorry {username}, it seems that you have not yet created a backlog, if you would\
    #             like to do so, simply type "/newBacklog in the chat. For further help type /help to get\
    #             a list of possible commands, or for a specific command type /help followed by said command.')

    return await ctx.send("/addGame not implemented")

@bot.command(name='delGame')
async def delGame(ctx, *args):
    return await ctx.send("/delGame not implemented.")

@bot.command(name='list')
async def list(ctx, *args):
    return await ctx.send("/list not implemented.")

@bot.command(name='suggestGames')
async def suggestGames(ctx, *args):
    return await ctx.send("/suggestGames not implemented.")

@bot.command(name='edit')
async def edit(ctx, *args):   
    return await ctx.send("/edit not implemented.")

@bot.command(name='fq')
async def fq(ctx, *args):
    return await ctx.send("/fq not implemented.")
    await ctx.send(response)

bot.run(TOKEN)