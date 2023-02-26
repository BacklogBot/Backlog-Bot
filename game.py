class Game:
    #initialize new game, with standard initialization interest=0,
    #avgTime=0, and genres as an empty list
    def __init__(self, name, interest=0, avgTime=0, genres=[], timePlayed=0):
        self.name=name
        #interst is intrest in the game directly
        self.interest=interest
        #avgTime is average time in a single play session
        self.avgTime=avgTime
        self.genres=genres
        #timePlayed is total time this game has played
        self.timePlayed=timePlayed

    #changes game name
    def changeName(self, name):
        self.name=name

    #changes interest in game
    def changeInterest(self, interest):
        self.interest=interest

    #changes avgTime
    def changeAvgTime(self, avgTime):
        self.avgTime=avgTime

    #adds genre(s) to the game
    def addGenres(self, genres):
        for genre in genres:
            #might not be super efficient, linear time
            if genre not in self.genres:
                self.genres.append(genre)

    #removes genre(s) from the game
    def removeGenres(self, genres):
        for genre in genres:
            #might not be super efficient, linear time
            if genre in self.genres:
                self.genres.remove(genre)

    #changes timePlayed
    def changeTimePlayed(self, timePlayed):
        self.timePlayed=timePlayed

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
    def getTimePlayde(self):
        return self.timePlayed

    #returns a grade of the game based on intersts and genres
    #currently very rudimentary
    def gradeGame(self):
        #temporary solution
        return self.interest
