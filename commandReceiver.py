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
        '''
        arguments: 
            backlog[] backlogs: A list of all backlogs, across all bot users
            str name: A string of a user-entered name, representing the game the user wishes to delete from their backlog.
            str username: The discord username of the user who invoked this comamnd.
        returns: 
            0 if game was removed from backlog
            1 if game was not removed from backlog
        modifies:
            backlog[] backlogs: A list of all backlogs, across all bot users
        Description: 
            This function takes user-entered info and deletes the game in their backlog that corresponds to the info.
        '''          
        return backlogs[username].deleteGame(name)

    def editGameRec(self, game, title, interest, avgTime, timePlayed, genres):
        '''
        arguments: 
            game game: The game object that the user wishes to edit.
            str title: A string of a user-entered name, representing the name of the game the user wishes to edit.
            int interest: An int of a user-entered value, representing the user's interest in playing this current game, on a scale of 1 to 10.
            str avgTime: A string of a user-entered time, representing the user's average play time for this game, in the form #:##. 
            str timePlayed: A string of a user-entered time, representing the amount of time this user has played this game so far, in the form #:##. 
            str[] genres: All the genres that classify this game.
        returns: 
            None
        modifies:
            game game: The game object that the user wishes to edit.
        Description: 
            This function takes user-entered info and associates it with an already-existing game in their backlog.
        '''      
        game.changeName(title)
        game.changeInterest(interest)
        game.changeAvgTime(avgTime)
        game.changeTimePlayed(timePlayed)
        game.replaceGenres(genres)

    def editBacklogTimeRec(self, backlogs, timeMsg, username):
        '''
        arguments: 
            backlog[] backlogs: A list of all backlogs, across all bot users
            str timeMsg: A string of a user-entered time, representing the amount of time this user has played this game so far, in the form #:##. 
            str username: The discord username of the user who invoked this comamnd.
        returns: 
            None
        modifies:
            backlog[] backlogs: A list of all backlogs, across all bot users
        Description: 
            This function takes a user-entered time and updates their backlog's available play time to this new time.
        '''     
        avgTime = extractTime(timeMsg.content)
        backlogs[username].avgAvailableTime = avgTime    
 
    def editBacklogGenRec(self, backlogs, genresMsg, username):
        '''
        arguments: 
            backlog[] backlogs: A list of all backlogs, across all bot users
            str genresMsg: A string of user-entered preferred genres, seperated by spaces.
            str username: The discord username of the user who invoked this comamnd.
        returns: 
            None
        modifies:
            backlog[] backlogs: A list of all backlogs, across all bot users
        Description: 
            This function takes a user-entered string of genres, seperated by commas, and updates their backlog's preferred genres to this string.
        '''            
        newGenres = set(genresMsg.content.split())
        backlogs[username].userGenres = newGenres

    def listRec(self, backlogs, username):
        '''
        arguments: 
            backlog[] backlogs: A list of all backlogs, across all bot users
            str username: The discord username of the user who invoked this comamnd.
        returns: 
            str strng: A string representing a formatted response to the user. The response details all the games in their backlog.
        modifies:
            None
        Description: 
            This function lists a user's backlog games.
        '''    
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

    def SuggestGamesRec(self, backlogs, username, maxToList = 20):
        '''
        arguments: 
            backlog[] backlogs: A list of all backlogs, across all bot users
            str username: The discord username of the user who invoked this comamnd.
        returns: 
            str resp: A string representing a formatted response to the user. The response details all the backlog games that the user should play, from most to least likely to enjoy.
        modifies:
            None
        Description: 
            This function lists game suggestions for a user, based on their backlog.
        '''      
        #get a list of games coupled with their grades
        gamesGrades = []
        for game in backlogs[username].catalog:
            grade = backlogs[username].gradeGame(game)
            gamesGrades.append( (game,grade) )
        
        #sort from highest to lowest scored game
        gamesGrades.sort(key = lambda a: a[1], reverse=True) #descending
        
        #create a message containing the results to return
        resp = ""
        if maxToList > len(gamesGrades):
            maxToList = len(gamesGrades)
        for i in range(maxToList):
            tup = gamesGrades[i]
            resp += (tup[0].getName() + " with a score of " + str(tup[1]) + "\n")     
        return resp

    def helpBacklogRec(self, selected):
        '''
        arguments: 
            str selected: The command that the user has entered as an argument, representing the command they wish to see more info for
        returns: 
            str ret: A string that either tells the user their input was invalid or detailed information about the command they entered.
        modifies:
            None
        Description: 
            This command provides a detailed explanation of a user-entered command, if valid.
        '''          
        functionality = {
            'newBacklog': "/newBacklog: Generates a new backlog for a user which tracks the user's preferences in terms of veidogame genres and the average amounto time.\
daily that they have to play games.",\

            'addGame': "/addGame: Adds a game to your backlog. When adding a game, the user will be prompted for the game's name, genres, average time to completion, as well \
as how many hours they have alrady played the game and their current interest in it out of 10.",\

            'deleteGame': "/deleteGame {game title}: Removes the game with the matching title from your backlog. If the title of the game is seperated by spaces, enclose the title \
in quotes. For example: 'Super Mario'.",\

            'suggestGames': "/suggestGames {number of games}: Recommends up to the provided number of games. Using the command without specifying a number of games will automatically \
display up to the first 20 games in the user's backlog. Games will be listed alongside their calculated score in descending order. A higher score is indicative \
of games which more closely match the user's specified preferences and vise versa.",\

            'list': "/list {number of games}: Lists up to the provided number of games in the backlog in no particular order. If no number of games is specified, then all of the games \
in the user's backlog are listed.",\

            'editGame': "/editGame {game title}: Allows the user to edit the given game's information in the backlog. This includes the game's title, genres, average time to completion, time played, \
and user interest. If title of the game is seperated by spaces, enclose the title in quotes. For example: 'Super Mario'.",\

            'editBacklog': "/editBacklog: Allows the users to edit their backlog's recorded preferences, including the user's prefered genres and daily average available time."\
        }
        ret = ""
        if selected not in functionality:
            ret = "Unknown command, enter \"/helpBacklog\" for a comprehensive list of commands and their uses"
        else:
            ret = functionality[selected]
        return ret