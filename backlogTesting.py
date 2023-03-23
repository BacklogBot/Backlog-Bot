from backlog import Backlog
from game import Game
import unittest

class testBacklogMethods(unittest.TestCase):
    
    def testInitBacklog1(self): #test constructor with all the arguments
        testBacklog = Backlog("user1", {"RPG", "funny", "bullet hell"}, 2)
        self.assertEqual(testBacklog.username,"user1")
        self.assertEqual(testBacklog.catalog, [])
        self.assertEqual(testBacklog.length, 0)
        self.assertEqual(testBacklog.userGenres, {"RPG", "funny", "bullet hell"})
        self.assertEqual(testBacklog.avgAvailableTime, 2)

    def testInitBacklog2(self): #test constructor using default avTime argument
        testBacklog = Backlog("user1", {"RPG", "funny", "bullet hell"})
        self.assertEqual(testBacklog.username,"user1")
        self.assertEqual(testBacklog.catalog, [])
        self.assertEqual(testBacklog.length, 0)
        self.assertEqual(testBacklog.userGenres, {"RPG", "funny", "bullet hell"})
        self.assertEqual(testBacklog.avgAvailableTime, 0)

    def testInitBacklog3(self): #test constructor using default genres argument
        testBacklog = Backlog("user1", avgTime = 2)
        self.assertEqual(testBacklog.username,"user1")
        self.assertEqual(testBacklog.catalog, [])
        self.assertEqual(testBacklog.length, 0)
        self.assertEqual(testBacklog.userGenres, set())
        self.assertEqual(testBacklog.avgAvailableTime, 2)

    def testInitBacklog4(self): #test constructor using default genres and avgTime arguments
        testBacklog = Backlog("user1")
        self.assertEqual(testBacklog.username,"user1")
        self.assertEqual(testBacklog.catalog, [])
        self.assertEqual(testBacklog.length, 0)
        self.assertEqual(testBacklog.userGenres, set())
        self.assertEqual(testBacklog.avgAvailableTime, 0)

    def testAddGenre(self):
        testBacklog = Backlog("user1", {"RPG", "funny", "bullet hell"}, 2)
        testBacklog.addGenre("MMO")
        self.assertTrue("MMO" in testBacklog.userGenres)

    def testDelGenre1(self):
        testBacklog = Backlog("user1", {"RPG", "funny", "bullet hell"}, 2)
        testBacklog.delGenre("RPG")
        self.assertTrue("RPG" not in testBacklog.userGenres)

    def testDelGenre2(self):
        testBacklog = Backlog("user1", {"RPG", "funny", "bullet hell"}, 2)
        self.assertTrue(testBacklog.delGenre("MMO") == 1)

    def testAddGame(self):
        testBacklog = Backlog("user1", {"RPG", "funny", "bullet hell"}, 2)
        testGame = Game("Undertale", 10, 1, {"RPG", "funny", "bullet hell"}, 0)
        testBacklog.addGame(testGame)
        self.assertTrue(testGame in testBacklog.catalog)

    def testDelGame1(self):
        testBacklog = Backlog("user1", {"RPG", "funny", "bullet hell"}, 2)
        testGame = Game("Undertale", 10, 1, {"RPG", "funny", "bullet hell"}, 0)
        testBacklog.addGame(testGame)
        testBacklog.delGame(testGame)
        self.assertTrue(testGame not in testBacklog.catalog)

    def testDelGame2(self):
        testBacklog = Backlog("user1", {"RPG", "funny", "bullet hell"}, 2)
        self.assertTrue(testBacklog.delGame("Undertale") == 1)

    def testGetGame1(self):
        testBacklog = Backlog("user1", {"RPG", "funny", "bullet hell"}, 2)
        testGame = Game("Undertale", 10, 1, {"RPG", "funny", "bullet hell"}, 0)
        testBacklog.addGame(testGame)
        self.assertEquals(testBacklog.getGame("Undertale"), testGame)

    def testGetGame2(self):
        testBacklog = Backlog("user1", {"RPG", "funny", "bullet hell"}, 2)
        self.assertEquals(testBacklog.getGame("Undertale"), None)

    def testGetUser(self):
        testBacklog = Backlog("user1", {"RPG", "funny", "bullet hell"}, 2)
        self.assertEquals(testBacklog.getUser, "user1")

    def testGetLength1(self):
        testBacklog = Backlog("user1", {"RPG", "funny", "bullet hell"}, 2)
        self.assertEquals(testBacklog.length, 0)

    def testGetLength2(self):
        testBacklog = Backlog("user1", {"RPG", "funny", "bullet hell"}, 2)
        testGame = Game("Undertale", 10, 1, {"RPG", "funny", "bullet hell"}, 0)
        testBacklog.addGame(testGame)
        self.assertEquals(testBacklog.length, 1)

if __name__ == '__main__':
    unittest.main()