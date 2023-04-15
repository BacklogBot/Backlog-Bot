#this is just an abstract class designed to set up the structure of Command objects 
import os
import random
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

from game import Game
import commandReceiver

from abc import ABC, abstractmethod #for abstract classes

def extractTime(timeStr):
    #expected timeStr format = hours:minutes
    time = timeStr.split(':')
    if len(time) == 1 or int(time[1]) == 0: #we only have hours to deal with
        return int(time[0])
    else:
        return int(time[0]) + int(time[1])/60.0

class Command(ABC):
    cr = commandReceiver.CommandReceiver()
    def __init__(self, bot, ctx, com_rec, args=None):
        self.bot = bot
        self.ctx = ctx #command context 
        self.username = ctx.message.author.name
        self.userID = int(ctx.author.id)
        self.args = args #command arguments 
        self.cr = com_rec  #receiver for this class
        
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
    async def execute(self): #variable checker functions
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

        self.cr.newBacklogRec(backlogs, genresMsg, timeMsg, self.username)

        #confirm backlog creation 
        return await self.ctx.send("{}'s backlog created!".format(self.username))


class AddGame(Command):
    def duplicateCheck(self, backlog, nameMsg):
        for i in range(len(backlog.catalog)):
            current_name = (backlog.catalog[i]).getName()
            name = nameMsg.content
            
            if current_name == name:
                return -1
        return 1

    async def execute(self, backlogs):
        if self.username not in backlogs: 
            return await self.ctx.send("You have yet to create a backlog, {}. Enter /helpBacklog for more info.".format(self.username))
        else:
            #prompt the user for the game's name
            await self.ctx.send("Please enter the game's name.")
            nameMsg = await self.waitForResponse(self.checkUser)



            while self.duplicateCheck(backlogs[self.username], nameMsg) == -1:
                await self.ctx.send('You cannot add this game to your backlog, {}. There is already a game with the same name in your backlog. Please enter a different name for the game.'.format(self.username))	
                nameMsg = await self.waitForResponse(self.checkUser)


            #prompt the user for the the game's genres
            await self.ctx.send("Please enter the game's genre(s) seperated by spaces.")
            genresMsg = await self.waitForResponse(self.checkUser)

            #prompt the user for the estimated time of the game 
            await self.ctx.send("Please enter how long the games take on average in hours in the format of hours:00.")
            avgTimeMsg = await self.waitForResponse(self.checkTimeFormat)

            #prompt the user for the amount of time played
            await self.ctx.send("Please enter how long you have already played this game in hours in the format of hours:00.\nEnter 0:00 if you have yet to play it.")
            timePlayedMsg = await self.waitForResponse(self.checkTimeFormat)

            #prompt the user for the their current interest in the game 
            await self.ctx.send("Please enter your current interest in the game, out of 10.")
            interestMsg = await self.waitForResponse(self.checkIntFormat)

            self.cr.addGameRec(backlogs, timePlayedMsg, interestMsg, avgTimeMsg, genresMsg, nameMsg, self.username)
            return await self.ctx.send('Successfully added this new game to your backlog {}.'.format(self.username))	

class DeleteGame(Command):
	async def execute(self, backlogs):
		name = self.args[0]
		if(self.cr.deleteGameRec(backlogs, name, self.username)): #if backlog could not find said game to remove
			return await self.ctx.send("{} was not found in your backlog, {}".format(name, self.username))
		else:
			return await self.ctx.send("{} was removed from your backlog, {}".format(name, self.username))

#May need to modify function to reduce coupling
class EditGame(Command):
    async def execute(self, backlogs):
        if self.username not in backlogs:#checks if backlog exists
            return await self.ctx.send('I am sorry {}, it seems that you have not yet created a backlog, if you would \
            to do so, simply type "/newBacklog in the chat. For further help enter /helpBacklog, then enter newBacklog.'.format(self.username))

        game_name = self.args[0]
        game_id = self.args[1]
        game = backlogs[self.username].getGameFromID(game_id) #The game being edited
        if(game == None): #if backlog could not find said game to edit
            return await self.ctx.send("{} was not found in your backlog, {}".format(game_name, self.username))
        
        #NOTE: cant pass this block off to the receiver because this is how we save the user requested attribute to change
        title = game.getName()#technically not needed
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

            change = (await self.waitForResponse(self.checkUser)).content
            if (change.lower()=="title"):
                await self.ctx.send("Please enter the title of the game you would like to add to your backlog.")
                title = (await self.waitForResponse(self.checkUser)).content
            elif (change.lower()=="genres"):
                await self.ctx.send("Please list the genres of the game in question such as RPG, MMO, Sandbox, etc. separated by spaces.")
                response = (await self.waitForResponse(self.checkUser)).content
                genres = set(response.split())
            elif (change.lower()=="average time of completion"):
                await self.ctx.send("Please enter how much time the game takes on average. For example, \"1:30\" for 1 hour and 30 minutes..")
                response = (await self.waitForResponse(self.checkUser)).content
                avgTime = extractTime(response)
            elif (change.lower()=="time played"):
                await self.ctx.send("Please enter how much time you have already played this game if at all. For example, \"1:30\" for 1 hour and 30 minutes or \"0:0\" if you have yet to play this game.")
                response = (await self.waitForResponse(self.checkUser)).content
                timePlayed = extractTime(response)
            elif (change.lower()=="initial interest"):
                await self.ctx.send("On a scale from 1 to 10 what would you rate your initial interest in this game?")
                response = (await self.waitForResponse(self.checkUser)).content
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
            response = (await self.waitForResponse(self.checkUser)).content
            if(response.lower()=="yes" or response.lower()=="y"):
                editing = False
        
        self.cr.editGameRec(game, title, interest, avgTime, timePlayed, genres)

        return await self.ctx.send("{} has been successfully edited!".format(title))
            

class EditBacklog(Command):
    async def execute(self, backlogs):
        #NOTE: consider regrading all the backlog games based on the new proposed change
        #basically call "regrade" at the end of this function, no matter which option was selected
        if self.username not in backlogs: 
            return await self.ctx.send("You have yet to create a backlog, {}. Enter /helpBacklog for more info.".format(self.username))
        else:			
            await self.ctx.send("If you wish to edit your backlog's preferred genres, enter 1.\nIf you wish to edit your average available playing time, enter 2.")			
            editMsg = await self.waitForResponse(self.checkUser)
            flag = 1

            while flag==1: #while they are entering *something*
                if editMsg.content == "1":
                    #edit genre
                    await self.ctx.send("Please enter a list of your prefered genres, seperated by spaces.")
                    genresMsg = await self.waitForResponse(self.checkUser)					
                    
                    self.cr.editBacklogGenRec(backlogs, genresMsg, self.username)
                    flag = 0

                elif editMsg.content == "2":
                    #edit time
                    await self.ctx.send("Please enter your average amount of available playtime in the format of hours:minutes.")
                    timeMsg = await self.waitForResponse(self.checkTimeFormat)	

                    self.cr.editBacklogTimeRec(backlogs, timeMsg, self.username)
                    flag = 0
                else:
                    await self.ctx.send("Invalid input. Try again.")
                    await self.ctx.send("If you wish to edit your backlog's preferred genres, enter 1.\nIf you wish to edit your average available playing time, enter 2.")			
                    editMsg = await self.waitForResponse(self.checkUser)		

        await self.ctx.send(self.username + "'s Backlog\n" + '='*15+"\n")  
        await self.ctx.send("Genre(s): " + str(backlogs[self.username].userGenres))
        await self.ctx.send("\nAverage Available Time: " + str(backlogs[self.username].avgAvailableTime)  )
        await self.ctx.send('='*50+"\n")          
        return await self.ctx.send("Backlog Updated!")  

class List(Command):
    async def execute(self, backlogs):
        if self.username not in backlogs: 
            return await self.ctx.send("You have yet to create a backlog, {}. Enter /helpBacklog for more info.".format(self.username))
        else:
            return await self.ctx.send(self.cr.listRec(backlogs, self.username))

class SuggestGames(Command):
    async def execute(self, backlogs):
        #list games in order of their scores, higher scores first  
        if self.username not in backlogs:
            return await self.ctx.send("You have yet to create a backlog, {}. Enter /helpBacklog for more info.".format(self.username))
        else:
            return await self.ctx.send(self.cr.SuggestGamesRec(backlogs, self.username))


class HelpBacklog(Command):
    async def execute(self): 

        if(self.args == None or len(self.args) == 0):
            await self.ctx.send("Here is a list of commands. Enter /helpBacklog and a command name for a description of the command's functionality.)\n")
            await self.ctx.send("NewBacklog\nAddGame\nDeleteGame\nEditGame\nEditBacklog\nList\nSuggestGames")
            return
        else:
            return await self.ctx.send( self.cr.helpBacklogRec(self.args[0]) )


