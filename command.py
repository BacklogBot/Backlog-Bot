#this is just an abstract class designed to set up the structure of Command objects 
import os
import random
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

from game import Game
from backlog import Backlog

from abc import ABC, abstractmethod #for abstract classes

def extractTime(timeStr):
	#time string take the format of hours:minutes

	time = timeStr.split(':')
	return int(time[0]) + 60/int(time[1])


class Command(ABC):
	def __init__(self, bot, ctx, args=None):
		self.bot = bot
		self.ctx = ctx #command context 
		self.username = ctx.message.author.name
		self.userID = int(ctx.author.id)
		self.args = args #command arguments 

	#returns true if the author of the message mathces the author of the command 
	def checkUser(self, msg):
		if(int(msg.author.id) != self.userID):
			return False
		else:
			return True

	#returns true if the message has the correct time format and the author matches the command author
	#and false otherwise  
	def checkTimeFormat(self, msg):
		time = msg.content.split(':')

		if(len(time) != 2): #check for a correct number of time denominations 
			return False
		elif(not time[0].isdigit()): #ensure the number of hours is an integer
			return False
		elif(not time[1].isdigit()): #ensure the number of minutes is an integer 
			return False
		elif((int(time[0]) >= 24) or (int(time[1]) >= 60)): #ensure the time is below the maximum 
			return False
		else:
			return (True and self.checkUser(msg)) 

	#returns true if the message is an integer and the athor matches the author of the command 
	#and false otherwise
	def checkIntFormat(self, msg):
		return msg.content.isdigit() and self.checkUser(msg)

	#waits for a response which matches the format as specified by the checkFunc function which
	#takes a msg and return either true or false depending on whether the message matches the conditions. 
	#If there is no response in specified time limit in minutes, the fucntion times out. 
	async def waitForResponse(self, checkFunc, time=5):
		try:
			msg = await self.bot.wait_for("message", check=checkFunc, timeout= time * 60) 
		except asyncio.TimeoutError:
			return await self.ctx.send('{}, your request timed out.'.format(self.username)) 
		return msg

	@abstractmethod #execution method responsbile for executing said command 
	async def execute(self, backlogs): #variable checker functions
		pass

#-------------------------------------------------------------------------------------------------------------------------------

class NewBacklog(Command):
	async def execute(self, backlogs):

	    #check to see if the user already has a backlog
	    if self.username in backlogs:
	        return await ctx.send('You already have an existing backlog.') 

	    #prompt the user for their list of prefered genres
	    await self.ctx.send("Please enter a list of your prefered genres.")
	    genresMsg = await self.waitForResponse(self.checkUser)

	    #prompt the user for average amount of available playtime in a day
	    await self.ctx.send("Please enter a enter your average amount of available playtime.")
	    timeMsg = await self.waitForResponse(self.checkTimeFormat)

	    #add the backlog to the backglogs dictionary
	    genres =  set(genresMsg.content.split())
	    avgTime = extractTime(timeMsg.content)

	    backlogs[self.username] = Backlog(self.username, genres, avgTime)

	    #confirm backlog creation 
	    return await self.ctx.send("{}'s backlog created!".format(self.username))

class AddGame(Command):
	async def execute(self, backlogs):
	    if self.username not in backlogs:
	        return await self.ctx.send('I am sorry {}, it seems that you have not yet created a backlog, if you would \
	                            to do so, simply type "/newBacklog in the chat. For further help type /help to get \
	                            a list of possible commands, or for a specific command type /help followed by said \
	                            command.'.format(self.username))

	    #prompt the user for the game's name
	    await self.ctx.send("Please enter the game's name.")
	    nameMsg = await self.waitForResponse(self.checkUser)

	    #prompt the user for the the game's genres
	    await self.ctx.send("Please enter the game's genres seperated by spaces.")
	    genresMsg = await self.waitForResponse(self.checkUser)

	    #prompt the user for the estimated time of the game 
	    await self.ctx.send("Please enter how long the games take on average in hours.")
	    avgTimeMsg = await self.waitForResponse(self.checkTimeFormat)

	    #prompt the user for the amount of time played
	    await self.ctx.send("Please enter how long you have already played this game in hours, entering 0 if you have yet to play it.")
	    timePlayedMsg = await self.waitForResponse(self.checkTimeFormat)

	    #prompt the user for the their current interest in the game 
	    await self.ctx.send("Please enter your current interest in the game, out of 10.")
	    interestMsg = await self.waitForResponse(self.checkIntFormat)

	    name = nameMsg.content
	    genres = set(genresMsg.content.split())
	    avgTime = extractTime(avgTimeMsg.content)
	    timePlayed = extractTime(timePlayedMsg.content)
	    interest = int(interestMsg.content)

	    backlogs[self.username].addGame(Game(name, interest, avgTime, genres, timePlayed))	

	    return await self.ctx.send('{} successfully added to your backlog {}.'.format(name, self.username))	

class DelGame():
	async def execute(self, backlogs):
		name = self.args[0]
		if(backlogs[self.username].delGame(name)): #if backlog could not find said game to remove
			return await self.ctx.send("{} was not found in your backlog, {}".format(name, username))
		else:
			return await self.ctx.send("{} was removed from your backlog, {}".format(name, username))

# class EditGame():
# 	def __init__(self):

# class EditBacklog():
# 	def __init__(self):

# class List():
# 	def __init__(self):

class SuggestGames(Command):
	async def execute(self, backlogs):
		#list games in order of their scores, higher scores first  
		if self.username not in backlogs: #temporary implementation with no arguments 
			await self.ctx.send("You have yet to create a backlog, {}".format(self.username))
		else:
			return await self.ctx.send(str(backlogs[self.username]))


# class helpBacklog():
# 	def __init__(self, *arg):


