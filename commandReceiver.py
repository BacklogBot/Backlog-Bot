import backlog
import game
from game import Game

def extractTime(timeStr):
    '''
    arguments: 
        str timeStr: The string of time that the user entered, in the form of #:##.
    returns: 
        int ret: The time provided, in hours.
    modifies:
        None
    Description: 
        This function parses and returns and some provided time, in hours.
    '''
    time = timeStr.split(':')
    ret = -1
    if len(time) == 1 or int(time[1]) == 0: #we only have hours to deal with
        ret = int(time[0])
    else:
        ret = int(time[0]) + int(time[1])/60.0
    return ret

class CommandReceiver:
    def newBacklogRec(self, backlogs, genresMsg, timeMsg, username):
        '''
        arguments: 
            backlog[] backlogs: A list of all backlogs, across all bot users
            str genresMsg: A string of user-entered preferred genres, seperated by spaces. 
            str timeMsg: A string of a user-entered time, representing available playing time, in the form #:##. 
            str username: The discord username of the user who invoked this comamnd.
        returns: 
            None
        modifies:
            backlog[] backlogs: A list of all backlogs, across all bot users
        Description: 
            This function takes user-entered info and associates it with a new backlog.
        '''
        genres =  set(genresMsg.content.split())
        avgTime = extractTime(timeMsg.content)
        backlogs[username] = backlog.Backlog(username, genres, avgTime)  

    def addGameRec(self, backlogs, timePlayedMsg, interestMsg, avgTimeMsg, genresMsg, nameMsg, username):
        '''
        arguments: 
            backlog[] backlogs: A list of all backlogs, across all bot users
            str timePlayedMsg: A string of a user-entered time, representing the amount of time this user has played this game so far, in the form #:##. 
            str interestMsg: A string of a user-entered number, representing their interest in this game from 1 to 10.
            str avgTimeMsg: A string of a user-entered time, representing the user's average play time for this game, in the form #:##. 
            str genresMsg: A string of user-entered preferred genres, seperated by spaces.
            str nameMsg: The name of this new game.
            str username: The discord username of the user who invoked this comamnd.
        returns: 
            None
        modifies:
            backlog[] backlogs: A list of all backlogs, across all bot users
        Description: 
            This function takes user-entered info and associates it with a new game, which is then added into this user's backlog.
        '''        
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
        backlogs[username].avgAvailableTime = avgTime    
 
    def editBacklogGenRec(self, backlogs, genresMsg, username):
        new_genres = set(genresMsg.content.split())
        backlogs[username].userGenres = new_genres

    def listRec(self, backlogs, username):
        border = "=" * 75
        user = username
        back = user + "'s Backlog"
        strng = border + "\n" + back + "\n" + border + "\n"
        lst = backlogs[username].catalog
        i = 1
        for game in lst:
            strng += "{}: {}\n".format(i, game.getName())
            i += 1    
        return strng

    def SuggestGamesRec(self, backlogs, username):
        games_grades = []
        for game in backlogs[username].catalog:
            grade = backlogs[username].gradeGame(game)
            games_grades.append( (game,grade) )
        
        games_grades.sort(key = lambda a: a[1], reverse=True) #descending
        for item in games_grades:
            resp += (item[0] + " with a score of " + str(item[1]) + "\n")     
        return resp

    def helpBacklogRec(self, selected):
        functionality = {
            'newBacklog': "/newBacklog: Initializes backlog for a user",\
            'addGame': "/addGame: Adds a game to your backlog",\
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
