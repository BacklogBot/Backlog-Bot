import game

class Backlog:
	def __init__(self, username)
		self.username = username #discord username
		self.catalog = [] #list of games
		self.length = 0

	def __str__(self):
		formattedString = ""

		for game in catalog:
			name = game.getName()
			score = game.gradeGame()

			right_padding = ('{: <5}'.format(string))
			formattedString += '- SCORE: {: <2} ... GAME: {}\n'.format(score, name)

		return formattedString

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
				return 0 #return success 0 if there the game exists in the catlog and is removed 

		return 1 #return failure 1 if there is no such game in the catalog

	#returns the username of whoever the backlog belondgs to 
	def getUser(self):
		return self.username

	#given a game's name, return the game object from the catalog, if it is not there then return None 
	def getGame(self, name):
		index = self.index(name)

		if(index == -1):
			return None
		else:
			return self.catalog[index]

	#returns the current length of the catalog
	def getLength(self):
		return self.length

