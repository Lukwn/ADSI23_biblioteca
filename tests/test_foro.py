import json
import random

from controller.LibraryController import LibraryController
from model import Connection
from . import BaseTestClass
from bs4 import BeautifulSoup
db = Connection()
library = LibraryController()
class TestForo(BaseTestClass):

    def test_gaiak_ikusi(self):
        self.login('jhon@gmail.com', '123')
        db.select("DELETE FROM Gaia")
        #ez badago gairik
        gaiak, count =library.search_gaiak("", 1)
        self.assertEqual(0, count)
        # gai bakarra
        library.add_gaia("proba_gaia")
        res = self.client.get('/foro?')
        gaiak, count = library.search_gaiak("", 1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, count)
        #gai bat baino gehiago
        library.add_gaia("proba_gaia_2")
        gaiak, count = library.search_gaiak("", 1)
        self.assertEqual(2, count)

    def test_gai_berria_sortu(self):
        self.login('jhon@gmail.com', '123')
        db.select("DELETE FROM Gaia")
        #gai hutsa ez dela sortu frogatu
        library.add_gaia("")
        gaiak, count = library.search_gaiak("", 1)
        self.assertEqual(0, count)
        #karaktere muga baino gehiagoko gaia ez dela sortu
        library.add_gaia("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut perspiciatis unde omnis iste natus error.")
        gaiak, count = library.search_gaiak("", 1)
        self.assertEqual(0, count)
        #gai berria sortu
        library.add_gaia("gai_berria")
        gaiak, count = library.search_gaiak("", 1)
        self.assertEqual(1, count)

    def test_komentarioak_ikusi(self):
        self.login('jhon@gmail.com', '123')
        db.select("DELETE FROM Gaia")
        library.add_gaia("Proba")
        db.select("DELETE FROM Komentario")
        #ez badago komentariorik
        komentarioak, count = library.search_komentarioak("1", 1)
        self.assertEqual(0, count)
        #komentarioa bakarra
        library.add_komentario(1, 2, "komentario_test", 0, "")
        komentarioak, count = library.search_komentarioak("1", 1)
        self.assertEqual(1, count)
        #gai bat baino gehiago
        library.add_komentario(1, 2, "komentario_test_2", 2, "komentario_test")
        komentarioak, count = library.search_komentarioak("1", 1)
        self.assertEqual(2, count)
        #erantzunak era egokian gordetzen dira
        res = db.select("SELECT gaia_id, user_id, txt, respondiendo_a, respondiendo_a_txt FROM Komentario WHERE respondiendo_a_txt='komentario_test'")[0]
        emaitza = (1, 2, "komentario_test_2", 2, "komentario_test")
        self.assertEqual(emaitza, res)
    def test_gehitu_komentarioa(self):
        self.login('jhon@gmail.com', '123')
        db.select("DELETE FROM Gaia")
        db.select("DELETE FROM Komentario")
        library.add_gaia("Proba")
        #komentario hutsa
        library.add_komentario(1, 2, "", 0, "")
        komentarioak, count = library.search_komentarioak("1", 1)
        self.assertEqual(0, count)
        #Gehiegizko karaktere
        library.add_komentario(1, 2, "The quick brown fox jumps over the lazy dog. This sentence is a classic pangram. Pangrams are sentences that use every letter of the alphabet at least once. They are fun for typists! The quick brown fox becomes a typist's friend when practicing typing skills. Pangrams help improve keyboard proficiency.", 0, "")
        komentarioak, count = library.search_komentarioak("1", 1)
        self.assertEqual(0, count)
        #komentarioa gehitu
        library.add_komentario(1, 2, "komentario_test", 0, "")
        komentarioak, count = library.search_komentarioak("1", 1)
        self.assertEqual(1, count)
