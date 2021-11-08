from random import random
import base62, unittest, model
import unittest.mock as mock

from model import ID_SEED

class TestStringMethods(unittest.TestCase):
    #Test conversion from id to short url and back
    def test_IdToShortURL(self):
        id = 1000000
        shortUrl = base62.idToShortURL(id)
        returnId = base62.shortURLToId(shortUrl)
        self.assertEqual(id, returnId)

    def test_ModelCreateEntry(self):
        def choice1000(self, value):
            s = (ID_SEED/1000)
            s += 1
            return s

        with mock.patch('random.randrange', choice1000):
            shortUrl = model.createEntry("linkedin.com")
        self.assertEqual(shortUrl, 'qj')

    def test_ModelDeleteEntry(self):
        message = model.deleteEntryFromMap('qj')
        self.assertEqual(message, 'Successfully Deleted')

if __name__ == '__main__':
    unittest.main()
