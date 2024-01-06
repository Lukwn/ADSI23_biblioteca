from datetime import date, datetime

class Erreserba:
	def __init__(self, user_id, hasiera_data, book_id, bueltatze_data, bueltatu_da):
		self.user_id = user_id
		self.hasiera_data = hasiera_data
		self.book_id = book_id
		self.bueltatze_data = bueltatze_data
		self.bueltatu_da = bueltatu_da

	def datanDago(self):
		erreserba_data = datetime.strptime(self.bueltatze_data, "%Y-%m-%d").date()
		return erreserba_data < date.today() and self.bueltatu_da == 0

	def gaur_erreserbatuta(self, book_id):
		erreserba_data = datetime.strptime(self.hasiera_data, "%Y-%m-%d").date()
		return erreserba_data == date.today() and book_id == book_id