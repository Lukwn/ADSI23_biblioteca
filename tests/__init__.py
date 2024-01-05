import unittest
from controller import webServer
from model import Connection

class BaseTestClass(unittest.TestCase):
	def setUp(self):
		self.app = webServer.app
		self.client = self.app.test_client()
		self.db = Connection()
		
	def tearDown(self):
		pass

	def login(self, email, password):
		return self.client.post('/login', data=dict(
			email=email,
			password=password
		))

	def logout(self,):
		return self.client.get('/logout')

	def liburua_erreserbatu(self, book_id):
		url = f'/book?id={book_id}'
		return self.client.post(url, data=dict(
			erreserbatu=''))

	def liburua_bueltatu(self, book_id, user_id):
		url = f"/bueltatu_aukeratu?user={user_id}"
		return self.client.post(url, data = dict( liburu_id = book_id))