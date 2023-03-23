class Game:
    #initialize new game, with standard initialization interest=0,
    #avgTime=0, and genres as an empty list
    def __init__(self, name, interest=0, avgTime=0, genres=set(), timePlayed=0):
        self.name=name
        #interst is intrest in the game directly
        self.interest=interest
        #avgTime is average time in a single play session
        self.avgTime=avgTime
        self.genres=genres
        #timePlayed is total time this game has played
        self.timePlayed=timePlayed

    #changes timePlayed
    def changeTimePlayed(self, timePlayed):
        self.timePlayed=timePlayed
        return 0

    #returns name
    def getName(self):
        return self.name

    #returns interest
    def getInterest(self):
        return self.interest

    #returns avgTime
    def getAvgTime(self):
        return self.avgTime

    #returns list of genres
    def getGenres(self):
        return self.genres

    #returns timePlayed
    def getTimePlayed(self):
        return self.timePlayed

    #changes game name
    def changeName(self, name):
        self.name=name
        return 0

    #changes interest in game
    def changeInterest(self, interest):
        self.interest=interest
        return 0

    #changes avgTime
    def changeAvgTime(self, avgTime):
        self.avgTime=avgTime
        return 0

    #adds genre(s) to the game
    def addGenres(self, genres):
        for genre in genres: #changed generes to a set to increase efficiency
            self.genres.add(genre)
        return 0

    #removes genre(s) from the game
    def removeGenres(self, genres):
        for genre in genres:
            self.genres.remove(genre)
        return 0
        
    #replaces genres of game wit provided genre
    def replaceGenres(self, genres):
        self.removeGenres(self.getGenres().copy())
        self.addGenres(genres)
        return 0

    #returns a grade of the game based on intersts and genres
    #currently very rudimentary
    def gradeGame(self):
        #temporary solution
        return self.interest
