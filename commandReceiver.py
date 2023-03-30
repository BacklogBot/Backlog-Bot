import backlog
import algo2
import game

def extractTime(timeStr):
	#expected timeStr format = hours:minutes
	time = timeStr.split(':')
	if len(time) == 1 or int(time[1]) == 0: #we only have hours to deal with
		return int(time[0])
	else:
		return int(time[0]) + 60/int(time[1])


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
        return backlogs[username].delGame(name)

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
        strng = border + "\n" + back + "\n" + border
        lst = backlogs[username].catalog
        i = 1
        for game in lst:
            strng += i + ": " + game.getName() + "\n"
            i += 1    
        return strng

    def SuggestGamesRec(self, backlogs, username):
        l1 = backlogs[username].catalog
        l2 = list(l1)  #make a shallow copy of the list. so by the end of this code block, l2 should be unchanged
        algo2.sortGames(l1)
        resp = "These are the games in your backlog that I think you should play, according to the preferences you have provided so far.\nnote: the higher the score, the more you'll enjoy it!\n\n"
        #algo2.printList(l1)  print the list of games to the terminal
        for game in l1:
            resp += (game.getName() + " with a score of " + str(game.getInterest()) + "\n")    
        return resp

    def helpBacklogRec(self, selected):
            if selected == 'NewBacklog':
                return "/NewBacklog: Initializes backlog for a user"
            elif selected == 'AddGame':
                return "/AddGame [any game title]: Adds a game to your backlog"
            elif selected == 'DeleteGame':
                return "/DeleteGame [any game title]: Removes the game from your backlog"
            elif selected == 'SuggestGames':
                return "/SuggestGames [number of games]: Recommends up to the provided number of games. Use the command without a number for a default list of 20 games"
            elif selected == 'List':
                return "/List [number of games]: Lists up to the provided number of games in the backlog in no particular order, or all of them if no number is provided"
            elif selected == 'EditGame':
                return "/EditGame [any game title]: Edits the given game's information in the backlog"
            elif selected == 'EditBacklog':
                return "/EditBacklog: Edits preferences for the backlog, such as preferred genres and average play time"
            else:
                return "Unknown command, enter \"/helpBacklog\" for a comprehensive list of commands and their uses"