#this is just an abstract class designed to set up the structure of Command objects 
import os
import random
import discord
import asyncio
import algo2
from dotenv import load_dotenv
from discord.ext import commands

from game import Game
from backlog import Backlog

from abc import ABC, abstractmethod #for abstract classes

def extractTime(timeStr):
	#expected timeStr format = hours:minutes
	time = timeStr.split(':')
	if len(time) == 1: #we only have hours to deal with
		return int(time[0])
	else:
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
		await self.ctx.send("Please enter a list of your prefered genres, seperated by spaces.")
		genresMsg = await self.waitForResponse(self.checkUser)

	    #prompt the user for average amount of available playtime in a day
		await self.ctx.send("Please enter your average amount of available playtime in the format of hours:minutes.")
		timeMsg = await self.waitForResponse(self.checkTimeFormat)

	    #add the backlog to the backlogs dictionary
		genres =  set(genresMsg.content.split())
		avgTime = extractTime(timeMsg.content)

		backlogs[self.username] = Backlog(self.username, genres, avgTime)

	    #confirm backlog creation 
		return await self.ctx.send("{}'s backlog created!".format(self.username))

class AddGame(Command):
	async def execute(self, backlogs):
		if self.username not in backlogs: 
			await self.ctx.send("You have yet to create a backlog, {}. Enter /help newBacklog for more info.".format(self.username))
		else:
			#prompt the user for the game's name
			await self.ctx.send("Please enter the game's name.")
			nameMsg = await self.waitForResponse(self.checkUser)

			#prompt the user for the the game's genres
			await self.ctx.send("Please enter the game's genre(s) seperated by spaces.")
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

#May need to modify function to reduce coupling
class EditGame():
	async def execute(self, backlogs):
		if self.username not in backlogs:#checks if backlog exists
			return await self.ctx.send('I am sorry {}, it seems that you have not yet created a backlog, if you would \
			to do so, simply type "/newBacklog in the chat. For further help type /help to get \
			a list of possible commands, or for a specific command type /help followed by said \
			command.'.format(self.username))

		name = self.args[0]
		game = backlogs[self.username].getGame(name) #The game being edited
		if(game!=None): #if backlog could not find said game to edit
			return await self.ctx.send("{} was not found in your backlog, {}".format(name, username))
		
		name = game.getName()#technically not needed
		genres = game.getGenres()
		avgTime = game.getAvgTime()
		timePlayed = game.getTimePlayed()
		interest = game.getInterest()
        
		editing = True
		while(editing):#loop to edit multiple attributes
			await self.ctx.send("Please type which attribute you would like to change.\n\n\
			- Title\n\
			- Genres\n\
			- Average Time of Completion\n\
			- Time Played\n\
			- Initial Interest")
			change = await self.waitForResponse(self.checkUser)
			if (change.lower()=="title"):
				await self.ctx.send("Please enter the title of the game you would like to add to your backlog.")
				title = await self.waitForResponse(self.checkUser)
			elif (change.lower()=="genres"):
				await self.ctx.send("Please list the genres of the game in question such as RPG, MMO, Sandbox, etc. separated by spaces.")
				response = await self.waitForResponse(self.checkUser)
				genres = set(response.content.split())
			elif (change.lower()=="average time of completion"):
				await self.ctx.send("Please enter how much time the game takes on average. For example, \"1:30\" for 1 hour and 30 minutes..")
				response = await self.waitForResponse(self.checkUser)
				avgTime = extractTime(response)
			elif (change.lower()=="time played"):
				await self.ctx.send("Please enter how much time you have already played this game if at all. For example, \"1:30\" for 1 hour and 30 minutes or \"0:0\" if you have yet to play this game.")
				response = await self.waitForResponse(self.checkUser)
				timePlayed = extractTime(response)
			elif (change.lower()=="interest"):
				await self.ctx.send("On a scale from 1 to 10 what would you rate your initial interest in this game?")
				response = await self.waitForResponse(self.checkUser)
				interest = int(response)
			else:
				await self.ctx.send("Response not recognized.")
            
            #checks if user is done editing
            #may need clarification
			await self.ctx.send("Is this information correct? Type yes or no.\n\n\
			-Game: {}\n\
			-Genres: {}\n\
			-Average Time of Completion: {}\n\
			-Time Played: {}\n\
			-Initial Interest: {}".format(title, genres, avgTime, timePlayed, interest))
			response = await self.waitForResponse(self.checkUser)
			if(response.lower()=="yes" or response.lower()=="y"):
				editing = False
        
		game.changeName(title)
		game.changeInterest(interest)
		game.changeAvgTime(avgTime)
		game.changeTimePlayed(timePlayed)
		game.replaceGenres(genres)
		return await self.ctx.send("{} has been successfully edited!".format(title))
            

class EditBacklog(Command):
	async def execute(self, backlogs):
		if self.username not in backlogs: 
			await self.ctx.send("You have yet to create a backlog, {}".format(self.username))
		else:			
			await self.ctx.send("If you wish to edit your backlog's preferred genres, enter 1.\nIf you wish to edit your average available playing time, enter 2.")			
			editMsg = await self.waitForResponse(self.checkUser)
			flag = 1

			while flag==1: #while they are entering *something*
				if editMsg.content == "1":
					#edit genre
					await self.ctx.send("Please enter a list of your prefered genres, seperated by spaces.")
					genresMsg = await self.waitForResponse(self.checkUser)					
					
					new_genres = set(genresMsg.content.split())
					backlogs[self.username].genres = new_genres
					flag = 0

				elif editMsg.content == "2":
					#edit time
					await self.ctx.send("Please enter your average amount of available playtime in the format of hours:minutes.")
					timeMsg = await self.waitForResponse(self.checkTimeFormat)	

					avgTime = extractTime(timeMsg.content)
					backlogs[self.username].avgTime = avgTime
					flag = 0
				else:
					await self.ctx.send("Invalid input. Try again.")
					await self.ctx.send("If you wish to edit your backlog's preferred genres, enter 1.\nIf you wish to edit your average available playing time, enter 2.")			
					editMsg = await self.waitForResponse(self.checkUser)		

		return await self.ctx.send("Backlog Updated!")  

class List(Command):
	async def execute(self, backlogs):
		if self.username not in backlogs: 
			await self.ctx.send("You have yet to create a backlog, {}".format(self.username))
		else:
			border = "=" * 75
			user = self.username
			back = user + "'s Backlog"
			strng = border + "\n" + back + "\n" + border
			lst = backlogs[self.username].catalog
			i = 1
			for game in lst:
				strng += i + ": " + game.getName() + "\n"
				i += 1
			return await self.ctx.send(strng)

class SuggestGames(Command):
	async def execute(self, backlogs):
		#list games in order of their scores, higher scores first  
		if self.username not in backlogs: #temporary implementation with no arguments 
			await self.ctx.send("You have yet to create a backlog, {}".format(self.username))
		else:
			l1 = backlogs[self.username].catalog
			l2 = list(l1)  #make a shallow copy of the list. so by the end of this code block, l2 should be unchanged
			algo2.sortGames(l1)
			resp = "These are the games in your backlog that I think you should play, according to the preferences you have provided so far.\nnote: the higher the score, the more you'll enjoy it!\n\n"
			#algo2.printList(l1)  print the list of games to the terminal
			for game in l1:
				resp += (game.getName() + " with a score of " + str(game.getInterest()) + "\n")
			return await self.ctx.send(resp)


class helpBacklog():
	async def execute(self):
		if self.args.length == 0:
			await self.ctx.send("Here is a list of commands. Enter /helpBacklog [command name] for a description of the command's functionality.)\n")
			commands = ['NewBacklog', 'AddGame', 'DeleteGame', 'EditGame', 'EditBacklog', 'List', 'SuggestGames']
			for i in commands:
				await self.ctx.send(i)
			return
		else:
			if self.arg[1] == 'NewBacklog':
				return await self.ctx.send("/NewBacklog: Initializes backlog for a user")
			elif self.arg[1] == 'AddGame':
				return await self.ctx.send("/AddGame [any game title]: Adds a game to your backlog")
			elif self.arg[1] == 'DeleteGame':
				return await self.ctx.send("/DeleteGame [any game title]: Removes the game from your backlog")
			elif self.arg[1] == 'SuggestGames':
				return await self.ctx.send("/SuggestGames [number of games]: Recommends up to the provided number of games. Use the command without a number for a default list of 20 games")
			elif self.arg[1] == 'List':
				return await self.ctx.send("/List [number of games]: Lists up to the provided number of games in the backlog in no particular order, or all of them if no number is provided")
			elif self.arg[1] == 'EditGame':
				return await self.ctx.send("/EditGame [any game title]: Edits the given game's information in the backlog")
			elif self.arg[1] == 'EditBacklog':
				return await self.ctx.send("/EditBacklog: Edits preferences for the backlog, such as preferred genres and average play time")
			else:
				return await self.ctx.send("Unknown command, enter \"/helpBacklog\" for a comprehensive list of commands and their uses")


