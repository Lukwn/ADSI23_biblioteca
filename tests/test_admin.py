from . import BaseTestClass
from bs4 import BeautifulSoup

class TestAdmin(BaseTestClass):

    def test_botoia_agertu(self):
        #admin denean botoia agertuko da
        res = self.login('james@gmail.com', '123456')
        self.assertEqual(302, res.status_code)
        self.assertEqual('/', res.location)
        res2 = self.client.get('/')
        page = BeautifulSoup(res2.data, features="html.parser")
        print(page)
        self.assertEqual('ADMIN', page.find('header').find('ul').find_all('li')[-1].get_text())

    def test_botoia_ez_agertu(self):
        #ez denean admin ez da agertuko botoia
        res = self.login('ejemplo@gmail.com', '123456')
        self.assertEqual(res.status_code, 302)
        self.assertEqual('/', res.location)
        res2 = self.client.get('/')
        page = BeautifulSoup(res2.data, features="html.parser")
        print(page)
        self.assertNotEqual('ADMIN', page.find('header').find('ul').find_all('li')[-1].get_text())


    def test_opzioak_ikusi(self):
        self.login('james@gmail.com', '123456')
        #Opzioak agertzen diren
        response = self.client.get('/admin')
        self.assertIn('Erabiltzailea ezabatu', response.text)
        self.assertIn('Erabiltzaile berria sartu', response.text)
        self.assertIn('Liburu berria sartu', response.text)