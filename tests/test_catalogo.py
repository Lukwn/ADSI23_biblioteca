from . import BaseTestClass
from bs4 import BeautifulSoup

class TestCatalogo(BaseTestClass):
	
	def test_sin_parametros_de_busqueda(self):
		res = self.client.get('/catalogue')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(6,len(page.find('div', class_='row').find_all('div', class_='card')))


	def test_busquedaFallida(self):
		params = {
			'title': "Este libro no existe"
		}
		res = self.client.get('/catalogue', query_string = params)
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(0, len(page.find('div', class_='row').find_all('div', class_='card')))

	def test_busquedaHarryPotter(self):
		params = {
			'title': "Harry Potter"
		}
		res = self.client.get('/catalogue', query_string = params)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(6, len(page.find('div', class_='row').find_all('div', class_='card')))
		for card in page.find('div', class_='row').find_all('div', class_='card'):
			self.assertIn(params['title'].lower(), card.find(class_='card-title').get_text().lower())
		self.assertEqual(2, len(page.find('ul', class_='pagination').find_all('li', class_='page-item')))


		



