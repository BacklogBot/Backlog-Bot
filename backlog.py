import game 

class Backlog:

    '''
    arguments: 
        str username: The discord username of the user 
        set<str> genres: The list of preferred videogame genres that the user has logged 
        int avgTime: The average amount of daily playtime in hours that the user has available
    returns:
        Backlog self: A newly created backlog. 
    modifies:
        str self.username: The discord username of the backlog's owner
        list<Game> self.catalog: The list of games which the user has entered into their backlog.
        set<str> self.userGenres: The list of the user's preferred genres.
        int self.avgAvailableTime: The average amount of available time that the owner has daily to play.   
    Despcription: 
        Constructs a new backlog for user.
    '''
    def __init__(self, username, genres = set(), avgTime = 0):
        #basic catalog attributes
        self.username = username #discord username
        self.catalog = [] #list of games 

        #client preferences
        self.userGenres = genres
        self.avgAvailableTime = avgTime


    '''
    arguments: 
        None
    returns: 
        str formattedString: A formatted string which represents the backlog. 
    modifies: 
        None
    Description: 
        This function converts a backlog into a string which includes each game in the backlog
        as well as that games corresponding score, calculated by the gradeGame algorithm. 
    '''
    def __str__(self):
        formattedString = "Backlog for {}:\n\n".format(self.username)

        for game in self.catalog:
            name = game.getName()
            score = game.gradeGame()

            formattedString += '- SCORE: {: <3} ... GAME: {}\n'.format(score, name)

        return formattedString

    '''
    arguments: 
        str genre: A string representing a game genre.
    returns: 
        int: Zero is returned upon function completion.  
    modifies: 
        set<str> self.userGenres:  The list of the user's preferred genres.
    Description: 
        This function adds a genre to backlog's list of prefered genres. 
    '''
    def addGenre(self, genre):
        self.userGenres.add(genre)
        return 0

    '''
    arguments: 
        str genre: A string representing a game genre.
    returns: 
        int: 0 if genre removed, 1 if no such genre existed in self.userGenres.  
    modifies: 
        set<str> self.userGenres:  The list of the user's preferred genres.
    Description: 
        This function removes the provided genre from the list of the preferred genres
        in the backlog. 
    '''
    def delGenre(self, genre):
        if(genre in self.userGenres):
            self.userGenres.remove(genre)
            return 0 #return 0 if genre was in userGenres and was removed 
        return 1 #return 1 if there is no such genre currently in userGenres 

    '''
    arguments: 
        str name: A string representing a the name of a game.
    returns: 
        int index: -1 if game not in catalog, the game's index otherwise
    modifies: 
        None
    Description: 
        This function goes through the catalog of games and finds the index
        of the game which has a name mathcing the one provided. 
    '''
    def index(self, name):
        if len(self.catalog) > 0:
            for index in range(len(self.catalog)):
                game = self.catalog[index]
                if(game.getName() == name):
                    return index
        return -1 #return -1 if the given title is not in the catalog

        '''
    arguments: 
        Game game: The game which the user wants to add the backlog.
    returns: 
        int: 0 upon successful completion, 1 otherwise.
    modifies: 
        list<Game> self.catalog: The list of games stored in the backlog. 
    Description: 
        Adds the provided game to the backlog. 
    '''
    def addGame(self, game):
        name = game.getName()

        if(len(self.catalog) == 0):
            self.catalog.append(game)
            return 0

        if(self.index(name) == -1): #there is no matching title in the catalog
            self.catalog.append(game)            
            return 0
        else: #there is a mathcing title in the catalog
            return 1

    '''
    arguments: 
        Game game: The game which the user wants to remove from the backlog.
    returns: 
        int: 0 upon successful completion, 1 otherwise.
    modifies: 
        list<Game> self.catalog: The list of games stored in the backlog. 
    Description: 
        Removes the provided game from the backlog. 
    '''
    def deleteGame(self, name):
        for index in range(len(self.catalog)):
            game = self.catalog[index]
            if(game.getName() == name):
                self.catalog.pop(index)
                return 0 #return success 0 if there the game exists in the catlog and is removed

        return 1 #return failure 1 if there is no such game in the catalog

    '''
    arguments: 
        None
    returns: 
        str self.username: The discord username of whoever owns the backlog.
    modifies: 
        None
    Description: 
        Provides the discord username of the whoever owns the backlog. 
    '''
    def getUser(self):
        return self.username

    '''
    arguments: 
        str name: The name of the game to be retrieved from the backlog 
    returns: 
        Game game: Game in the backlog's catalog who name matches the one given, None if no matching game
    modifies: 
        None
    Description: 
        Returns the Game object in the backlog, whose name matches the one provided. 
    '''
    def getGame(self, name):
        for i in range(len(self.catalog)):
            if self.catalog[i].getName() == name:
                    return self.catalog[i]
        return None

    '''
    arguments: 
        None
    returns: 
        int len: The number of games in the backlog catalog
    modifies: 
        None
    Description: 
        Returns the number games stored in the backlog. 
    '''
    def getLength(self):
        return len(self.catalog)
    
    '''
    arguments: 
        Game game: The game object which will be graded 
    returns: 
        int score: a score designed to represent the how 
    modifies: 
        None
    Description: 
        Provides the score of a game determined by a special algorithm which takes into
        the user interest in a game, the number mathcing genres between the game and the 
        users's prefered genres, and the difference between how long the game is and the 
        amount of time that the user has available to play daily.

    '''
    def gradeGame(self, game):
        score=game.getInterest()*100
        
        #matchingGenres=len(game.getGenres().intersection(self.userGenres()))
        gamesGenres = game.getGenres()
        preferredGenres = self.userGenres
        matchingGenres = gamesGenres.intersection(preferredGenres)
        matchingGenresLen = len(matchingGenres)
        
        score += matchingGenresLen*100
        score -= game.getTimePlayed()
        score -= min(0,game.getAvgTime()-self.avgAvailableTime)*600
        return score
