from . import BaseTestClass
from bs4 import BeautifulSoup


class TestCatalogo(BaseTestClass):

    def test_lagunGabe(self):
        res = self.login('ejemplo2@gmail.com', '123456') #erabilktzaile lagun gabea logeatu
        res = self.client.get('/gomendio')  #sortu
        self.assertEqual(200, res.status_code)  #ondo egin dela konprobatu
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(6, len(page.find('div', class_='row').find_all('div', class_='card')))

    def test_lagunGabe_irakurriak(self):
        res = self.login('pablo@gmail.com', '123456') #erabilktzaile lagun gabea logeatu
        res = self.client.get('/gomendio')  #sortu
        self.assertEqual(200, res.status_code)  #ondo egin dela konprobatu
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(6, len(page.find('div', class_='row').find_all('div', class_='card')))

    def test_lagunekin(self):
        res = self.login('jhon@gmail.com', '123') #erabilktzaile lagunduna logeatu
        res = self.client.get('/gomendio')  #sortu
        self.assertEqual(200, res.status_code)  #ondo egin dela konprobatu
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(4, len(page.find('div', class_='row').find_all('div', class_='card')))
        # kasu honetan 2 gomendio bakarrik irten beharko lirateke, James erabiltzailea begiratus 2 liburu gomendatu ahal dituelako bakarrik


    def test_lagunekinBainaLibururikEz(self):
        res = self.login('james@gmail.com', '123456') #erabilktzaile lagunduna (baiana liburu gabeak lagunak) logeatu
        res = self.client.get('/gomendio')  #sortu
        self.assertEqual(200, res.status_code)  #ondo egin dela konprobatu
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(6, len(page.find('div', class_='row').find_all('div', class_='card')))


