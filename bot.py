# bot.py
import os
import discord #pip install discord
import command
from dotenv import load_dotenv #pip install python-env
from discord.ext import commands

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

backlogs = dict() #dictionary which uses the member name as a key and the backglog as a value

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    #guild = server
    '''
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    '''

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
async def newBacklog(ctx, *args): #user typed /newBacklog
    cmd = command.NewBacklog(bot, ctx)
    return await cmd.execute(backlogs)


@bot.command(pass_context=True, name='addGame')
async def addGame(ctx, *args):
    cmd = command.AddGame(bot, ctx)
    return await cmd.execute(backlogs)

@bot.command(name='delGame')
async def delGame(ctx, *args):
    cmd = command.DelGame(bot, ctx, args)
    return await cmd.execute(backlogs)

@bot.command(name='list')
async def list(ctx, *args):
    cmd = command.List(bot, ctx)
    return await cmd.execute(backlogs)

@bot.command(name='suggestGames')
async def suggestGames(ctx, *args):
    cmd = command.SuggestGames(bot, ctx)
    return await cmd.execute(backlogs)

@bot.command(name='editBacklog')
async def edit(ctx, *args):
    cmd = command.EditBacklog(bot, ctx)
    return await cmd.execute(backlogs)

@bot.command(name='fq')
async def fq(ctx, *args):
    return await ctx.send("/fq not implemented.")

bot.run(TOKEN)
