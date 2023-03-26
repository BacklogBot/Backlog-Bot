import game 

class Backlog:
    def __init__(self, username, genres = set(), avgTime = 0):
        #basic catalog attributes
        self.username = username #discord username
        self.catalog = [] #list of games
        self.length = 0

        #client preferences
        self.userGenres = genres
        self.avgAvailableTime = avgTime

    def __str__(self):
        formattedString = "Backlog for {}:\n\n".format(self.username)

        for game in self.catalog:
            name = game.getName()
            score = game.gradeGame()

            formattedString += '- SCORE: {: <3} ... GAME: {}\n'.format(score, name)

        return formattedString

    #adds the specified genre to the backlog preferences
    def addGenre(self, genre):
        self.genres.add(genre)
        return 0

    #removes the specified genre from the backlog preferences
    def delGenre(self, genre):
        if(genre in self.userGenres):
            self.userGenres.remove(genre)
            return 0 #return 0 if genre was in userGenres and was removed 
        return 1 #return 1 if there is no such genre currently in userGenres 

    #take a game's name, finds its index in the catalog, if it is not in the catalog returns -1
    def index(self, name):
        for index in range(self.length):
            game = self.catalog[index]

            if(game.getName() == name):
                return index
        return -1 #return -1 if the given title is not in the catalog

    #adds a game object to the catalog
    def addGame(self, game):
        name = game.getName()

        if(self.length == 0):
            self.catalog.append(game)
            return 0

        if(self.index(name) == -1): #there is no matching title in the catalog
            for index in range(self.length):
                existingGame = self.catolog[index]

                if(existingGame.gradeGame() > game.gradeGame()):
                    self.catalog.insert(index, game)

            self.length += 1
            return 0
        else: #there is a mathcing title in the catlog
            return 1

    #takes a game's name, finds the matching game in the catalog, and removes it
    def delGame(self, name):
        for index in range(self.length):
            game = self.catalog[index]

            if(game.getName() == name):
                self.catalog.pop(index)
                self.length -= 1
                return 0 #return success 0 if there the game exists in the catlog and is removed

        return 1 #return failure 1 if there is no such game in the catalog

    #returns the username of whoever the backlog belondgs to
    def getUser(self):
        return self.username

    #given a game's unqiue id, return the game object from the catalog, if it is not there then return None
    def getGame(self, game_id):
        for i in range(len(self.catalog)):
            if self.catalog[i].getID() == int(game_id):
                    return self.catalog[i]
        return None

    #returns the current length of the catalog
    def getLength(self):
        return self.length
