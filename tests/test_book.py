from . import BaseTestClass
from bs4 import BeautifulSoup


class TestCatalogo(BaseTestClass):

    def test_liburu_egokia(self):
        params = {
            'id': 1
        }
        res = self.client.get('/book', query_string=params)
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(1, len(page.find('div', class_='card-body').find_all('h5', string='Ligeros libertinajes sabaticos')))

    def test_liburu_faltsua(self):
        params = {
            'id': 123001201
        }
        res = self.client.get('/book', query_string=params)
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(1, len(page.find('div', class_='card-body').find_all('h6', string='Liburua ez da existitzen')))