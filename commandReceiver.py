import backlog
import game
from game import Game

""" 
=====================================
    THIS BLOCK IS FOR SUGGESTGAMES
=====================================
"""
def printList(l):
    for i in range(len(l)):
        print(l[i].getName() + " with a score of " + str(l[i].getInterest()) ) 

def get_pivot(input_list, starting, ending):  #uses median of three method!
    middle = (starting+ending)//2  #get the average of the starting and ending indices
    pivot = ending

    #do a bunch of comparisons to choose the median item from starting, ending, and middle
    if input_list[starting].getInterest() < input_list[middle].getInterest():
        #if here, we already know starting < middle
        if input_list[middle].getInterest() < input_list[ending].getInterest():
            #starting < middle < ending
            pivot = middle
    elif input_list[starting].getInterest() < input_list[ending].getInterest():  
        #if here, we already know middle < starting and now we have starting < ending...middle < starting < ending
        pivot = starting
    #if we end up never reassigning pivot, we know the middle and starting are not the median which leaves ending as the only possibility
    return pivot

def compare(game1, game2):
    '''
    basically, we consider interest to have a higher weight than time played, while do our comparisons
    weight really comes into play when there needs to be tie-breakers
    '''
    if game1.getInterest() > game2.getInterest():
        return 1
    elif game1.getInterest() < game2.getInterest():
        return -1    
    else:
        if game1.getTimePlayed() > game2.getTimePlayed():
            return 1
        elif game1.getTimePlayed() < game2.getTimePlayed():
            return -1
        else:
            return 0            

def partition(input_list, starting, ending):
    pivot_index = get_pivot(input_list, starting, ending) #get the item we'll compare everything else to
    pivot_value = input_list[pivot_index]
    
    #move the pivot item into the leftmost position
    input_list[pivot_index] = input_list[starting]
    input_list[starting] = pivot_value

    border = starting
    for i in range(starting, ending+1): 
        if ( compare(input_list[i], input_list[starting]) == 1 ):
            border += 1 

            #swap the current item with the border item
            temp = input_list[i]
            input_list[i] = input_list[border]
            input_list[border] = temp
            #this ensures all items less than the pivot will be moved to the LHS of the list

    #after going through the whole list, swap the starting (which is now the pivot) and the border
    temp = input_list[starting]
    input_list[starting] = input_list[border]
    input_list[border] = temp

    return border 

def quicksort(input_list, starting, ending):
    #if there's more than 1 item to be sorted   
    if starting < ending: 
        pivot = partition(input_list, starting, ending)
        quicksort(input_list, starting, pivot-1)  #sort all items to the left of pivot
        quicksort(input_list, pivot+1, ending)  #sort all items to the right of pivot

def sortGames(input_list):  #uses quicksort to sort games
    quicksort(input_list, 0, len(input_list)-1) 

""" 
================================================
    THIS BLOCK IS FOR THE REST OF THE COMMANDS
================================================
"""

def extractTime(timeStr):
	#expected timeStr format = hours:minutes
	time = timeStr.split(':')
	if len(time) == 1 or int(time[1]) == 0: #we only have hours to deal with
		return int(time[0])
	else:
		return int(time[0]) + int(time[1])/60.0


class CommandReceiver:
    def newBacklogRec(self, backlogs, genresMsg, timeMsg, username):
        #add the backlog to the backlogs dictionary
        genres =  set(genresMsg.content.split())
        avgTime = extractTime(timeMsg.content)
        backlogs[username] = backlog.Backlog(username, genres, avgTime)  

    def addGameRec(self, backlogs, timePlayedMsg, interestMsg, avgTimeMsg, genresMsg, nameMsg, username):
        name = nameMsg.content
        genres = set(genresMsg.content.split())
        avgTime = extractTime(avgTimeMsg.content)
        timePlayed = extractTime(timePlayedMsg.content)
        interest = int(interestMsg.content)

        backlogs[username].addGame(game.Game(name, interest, avgTime, genres, timePlayed))	

    def deleteGameRec(self, backlogs, name, username):
        return backlogs[username].deleteGame(name)

    def editGameRec(self, game, title, interest, avgTime, timePlayed, genres):
        game.changeName(title)
        game.changeInterest(interest)
        game.changeAvgTime(avgTime)
        game.changeTimePlayed(timePlayed)
        game.replaceGenres(genres)

    def editBacklogTimeRec(self, backlogs, timeMsg, username):
        avgTime = extractTime(timeMsg.content)
        backlogs[username].avgTime = avgTime    
 
    def editBacklogGenRec(self, backlogs, timeMsg, username):
        new_genres = set(genresMsg.content.split())
        backlogs[username].genres = new_genres

    def listRec(self, backlogs, username):
        border = "=" * 75
        user = username
        back = user + "'s Backlog"
        strng = border + "\n" + back + "\n" + border + "\n"
        lst = backlogs[username].catalog
        i = 0
        for game in lst:
            strng += "{}: {}\n".format(i, game.getName())
            i += 1    
        return strng

    def SuggestGamesRec(self, backlogs, username):
        l1 = backlogs[username].catalog
        l2 = list(l1)  #make a shallow copy of the list. so by the end of this code block, l2 should be unchanged
        sortGames(l1)
        resp = "These are the games in your backlog that I think you should play, according to the preferences you have provided so far.\nnote: the higher the score, the more you'll enjoy it!\n\n"
        #algo2.printList(l1)  print the list of games to the terminal
        for game in l1:
            resp += (game.getName() + " with a score of " + str(game.getInterest()) + "\n")     
        return resp

    def helpBacklogRec(self, selected):
        functionality = {
            'newBacklog': "/newBacklog: Initializes backlog for a user",\
            'addGame': "/addGame [any game title]: Adds a game to your backlog",\
            'deleteGame': "/deleteGame [any game title]: Removes the game from your backlog",\
            'suggestGames': "/suggestGames [number of games]: Recommends up to the provided number of games. Use the command without a number for a default list of 20 games",\
            'list': "/list [number of games]: Lists up to the provided number of games in the backlog in no particular order, or all of them if no number is provided",\
            'editGame': "/editGame [any game title]: Edits the given game's information in the backlog",\
            'editBacklog': "/editBacklog: Edits preferences for the backlog, such as preferred genres and average play time"\
        }

        if selected not in functionality:
            return "Unknown command, enter \"/helpBacklog\" for a comprehensive list of commands and their uses"
        else:
            return functionality[selected]
