# bot.py
import os
import discord #pip install discord
from dotenv import load_dotenv #pip install python-env
from discord.ext import commands
import factory

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='/', intents = discord.Intents.all())

backlogs = dict() #dictionary which uses the member name as a key and the backlog as a value

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, I see you are a new user.'
    )

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
    #order a helpBacklog object from the command factory
    cf = factory.ConcreteCommandFactory(bot, ctx, args) 
    cmd = cf.createNewCommand("helpBacklog")
    return await cmd.execute()

@bot.command(pass_context=True, name='newBacklog')
async def newBacklog(ctx, *args):
    #order a newBacklog object from the command factory
    cf = factory.ConcreteCommandFactory(bot, ctx, args) 
    cmd = cf.createNewCommand("newBacklog")
    return await cmd.execute(backlogs)

@bot.command(pass_context=True, name='addGame')
async def addGame(ctx, *args):
    #order a addGame object from the command factory
    cf = factory.ConcreteCommandFactory(bot, ctx, args) 
    cmd = cf.createNewCommand("addGame")
    return await cmd.execute(backlogs)

@bot.command(name='deleteGame')
async def deleteGame(ctx, *args):
    #order a delGame object from the command factory
    cf = factory.ConcreteCommandFactory(bot, ctx, args) 
    cmd = cf.createNewCommand("delGame")
    return await cmd.execute(backlogs)

@bot.command(name='list')
async def list(ctx, *args):
    #order a list object from the command factory
    cf = factory.ConcreteCommandFactory(bot, ctx, args) 
    cmd = cf.createNewCommand("list")
    return await cmd.execute(backlogs)

@bot.command(name='suggestGames')
async def suggestGames(ctx, *args):
    #order a suggestGames object from the command factory
    cf = factory.ConcreteCommandFactory(bot, ctx, args) 
    cmd = cf.createNewCommand("suggestGames")
    return await cmd.execute(backlogs)

@bot.command(name='editGame')
async def editGame(ctx, *args):
    #order a editGame object from the command factory
    cf = factory.ConcreteCommandFactory(bot, ctx, args) 
    cmd = cf.createNewCommand("editGame")
    return await cmd.execute(backlogs)

@bot.command(name='editBacklog')
async def editBacklog(ctx, *args):
    #order a editBacklog object from the command factory
    cf = factory.ConcreteCommandFactory(bot, ctx, args) 
    cmd = cf.createNewCommand("editBacklog")
    return await cmd.execute(backlogs)

@bot.command(pass_context=True, name='copyGame')
async def copyGame(ctx, *args):
    #order a copyGame object from the command factory
    cf = factory.ConcreteCommandFactory(bot, ctx, args) 
    cmd = cf.createNewCommand("copyGame")
    return await cmd.execute(backlogs)

@bot.command(name='fq')
async def fq(ctx, *args):
    return await ctx.send("/fq not implemented.")

bot.run(TOKEN)
