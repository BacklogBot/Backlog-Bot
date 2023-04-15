from abc import ABC, abstractmethod

class Cloneable(ABC):
    @abstractmethod
    def clone():
        pass

class Game(Cloneable):
    
    '''
    arguments: 
        str name: The name of the game 
        int interest: The user's current interest in the game out of 10
        int avgTime: The average time in hours the game takes to complete
        set<str> genres: The game's genres
        int timePlayed: The time the user has already played in hours 
    returns: 
        Game self: a new Game object
    modifies:
        str self.name: The name of the game
        int self.interest: The user's interest in the game out of 10
        int self.avgTime: The average time in hours that game takes to complete 
        set<str> self.genres: The genres of the game 
        int timePlayed: The time in hours that the user has already played 
    Description: 
        This function creates and returns and new Game object.
    '''
    def __init__(self, name, interest=0, avgTime=0, genres=set(), timePlayed=0):
        self.name=name
        #interst is intrest in the game directly
        self.interest=interest
        #avgTime is average time in a single play session
        self.avgTime=avgTime
        self.genres=genres
        #timePlayed is total time this game has played
        self.timePlayed=timePlayed

    '''
    arguments: 
        int timePlayed: the amount of time that the user has played the game in hours 
    returns: 
        int: 0 is returned upon successful completion
    modifies: 
        self.timePlayed: The amount of time that the user has played the game
    Description: 
        Setter function to change the timePlayed attribute of a Game object to the new
        integer value specified.
    '''
    def changeTimePlayed(self, timePlayed):
        self.timePlayed=timePlayed
        return 0

    '''
    arguments: 
        None
    returns:
        str self.name: the name of the game object on which the function is being called 
    modifies: 
        None
    Description:
        Getter function to retriev the name of the Game object.  
    '''
    def getName(self):
        return self.name

    '''
    arguments: 
        None
    returns:
        int self.interest: The user's interest in the game out of 10 
    modifies: 
        None
    Description:
        Getter fucntion which returns the user's interest game with which this function is called. 
    '''
    def getInterest(self):
        return self.interest

    '''
    arguments: 
        None
    returns:
        int self.avgTime: The average amount of time that the game takes to complete in hours
    modifies: 
        None
    Description:
        Getter function which returns the game's average time to completion in hours.
    '''
    def getAvgTime(self):
        return self.avgTime

    '''
    arguments: 
        None
    returns:
        set<str> self.genres: Returns a copy of the set of the game's genres 
    modifies: 
        None
    Description:
        Getter function which returns a copy of the set of the game's genres
    '''
    def getGenres(self):
        return self.genres.copy()

    '''
    arguments: 
        None
    returns:
        int self.timePlayed: The amount of time in hours that the user has playe the game
    modifies: 
        None
    Description:
        Getter function which returns the amount of time, in hours, the user has already played the 
        game for which this function is being called 
    '''
    def getTimePlayed(self):
        return self.timePlayed

    '''
    arguments: 
        str name: The new name of the game you want change
    returns: 
        int: 0 upon successful completion 
    modifies: 
        str self.name: the name of the game object
    Description: 
        Setter function that changes the name of the Game object to the
        one provided.
    '''
    def changeName(self, name):
        self.name=name
        return 0

    '''
    arguments:
        int interest: The new interest in the game, out of 10 
    returns: 
        int: 0 upon successful completion
    modifies: 
        int self.interest: The old interest of the user in said game 
    Description: 
        Setter function that changes the interest level of the Game object to
        the one provided.
    '''
    def changeInterest(self, interest):
        self.interest=interest
        return 0

    '''
    arguments: 
        int avgTime: The new average time in hours to complete the game 
    returns: 
        int: 0 upon successful completion
    modifies: 
        int self.avgTime: The current average time to complete the game in hours.
    Description: 
        Setter function that changes the average completion time of the Game object
        to the one provided.
    '''
    def changeAvgTime(self, avgTime):
        self.avgTime=avgTime
        return 0

    '''
    arguments: 
        set<str> genres: The new set of genres which the user would like to the game
    returns: 
        int: 0 upon successful completion
    modifies: 
        set<str> self.genres: the current set of the game's genres
    Description: 
        Adds the set of genres to the current genres already stored in the game.
    '''
    def addGenres(self, genres):
        for genre in genres: 
            self.genres.add(genre)
        return 0

    '''
    arguments: 
        set<str> genres: the set of genres that user wants to remove the games current genres
    returns: 
        int: 0 upon successful completion
    modifies: 
        set<str> self.genres: the current set of the game's genres
    Description: 
        Removes the specified genres from the game's current genres set. I there are genres
        that do not exist in the current genres set, they are ignored. 
    '''
    def removeGenres(self, genres):
        for genre in genres.copy():
            self.genres.remove(genre)
        return 0
        
    '''
    arguments: 
        set<str> genres: the set of genres which the user will want to replace the cure 
    returns: 
        int: 0 upon successful completion 
    modifies: 
        set<str> self.genres: the current set of the game's genres
    Description: 
        The function replaces all the current genre's games with those provided.
    '''
    def replaceGenres(self, genres):
        self.removeGenres(self.getGenres().copy())
        self.addGenres(genres)
        return 0


    #function to be removed 
    def gradeGame(self):
        #temporary solution
        return self.interest

    '''
    arguments: 
        None
    returns:
        Game clone: returns a deep copy of the Game object
    modifies: 
        None
    Description:
        Function that returns a deep copy of the Game object in quesiton.  
    '''
    def clone(self):
        return Game(self.name, self.interest, self.avgTime, self.genres, self.timePlayed)