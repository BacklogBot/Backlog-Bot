from game import Game
import unittest

class testGameMethods(unittest.TestCase):
    
    def testInitGame(self):
        testGame = Game("Undertale", 10, 1, set(["RPG", "funny", "bullet hell"]), 0)
        self.assertEqual(testGame.name,"Undertale")
        self.assertEqual(testGame.interest,10)
        self.assertEqual(testGame.avgTime,1)
        self.assertEqual(testGame.genres,set(["RPG", "funny", "bullet hell"]))
        self.assertEqual(testGame.timePlayed,0)
    
    def testGetGame(self):
        testGame = Game("Undertale", 10, 1, set(["RPG", "funny", "bullet hell"]), 0)
        self.assertEqual(testGame.getName(),"Undertale")
        self.assertEqual(testGame.getInterest(),10)
        self.assertEqual(testGame.getAvgTime(),1)
        self.assertEqual(testGame.getGenres(),set(["RPG", "funny", "bullet hell"]))
        self.assertEqual(testGame.getTimePlayed(),0)
    
    def testChangeGame(self):
        testGame = Game("test", 5, 5, set(["test1", "test2"]), 5)
        testGame.changeName("Undertale")
        testGame.changeInterest(10)
        testGame.changeAvgTime(1)
        testGame.removeGenres(set(["test2","test1"]))
        testGame.addGenres(set(["RPG", "funny", "bullet hell"]))
        testGame.changeTimePlayed(0)
        self.assertEqual(testGame.name,"Undertale")
        self.assertEqual(testGame.interest,10)
        self.assertEqual(testGame.avgTime,1)
        self.assertEqual(testGame.genres,set(["RPG", "funny", "bullet hell"]))
        self.assertEqual(testGame.timePlayed,0)
        testGame.replaceGenres(set(["blurg"]))
        self.assertEqual(testGame.genres,set(["blurg"]))
    
    def testRemoveGetGenres(self):
        testGame = Game("test", 5, 5, set(["test1", "test2"]), 5)
        testGame.removeGenres(testGame.getGenres())
        testGame.addGenres(set(["RPG", "funny", "bullet hell"]))
        testGame.addGenres(testGame.getGenres())
        self.assertEqual(testGame.genres,set(["RPG", "funny", "bullet hell"]))
    
    def testScoreGame(self):
        testGame = Game("Undertale", 10, 1, set(["RPG", "funny", "bullet hell"]), 0)
        self.assertEqual(testGame.gradeGame(),10)
        
        
        
if __name__ == '__main__':
    unittest.main()