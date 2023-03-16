from game import Game
import unittest

class testGameMethods(unittest.TestCase):
    
    def testInitGame(self):
        testGame = Game("Undertale", 10, 1, ("RPG", "funny", "bullet hell"), 0)
        self.assertEqual(testGame.name,"Undertale")
        self.assertEqual(testGame.interest,10)
        self.assertEqual(testGame.avgTime,1)
        self.assertEqual(testGame.genres,("RPG", "funny", "bullet hell"))
        self.assertEqual(testGame.timePlayed,0)
        
        
        
if __name__ == '__main__':
    unittest.main()