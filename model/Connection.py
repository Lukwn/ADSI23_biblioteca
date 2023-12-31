import sqlite3

class Connection:
	__instance = None
	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(Connection, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance

	def __init__(self):
		if not self.__initialized:
			self.con = sqlite3.connect("datos.db", check_same_thread=False)
			self.cur = self.con.cursor()
			self.__initialized = True

	def select(self, sentence, parameters=None):
		if parameters:
			self.cur.execute(sentence, parameters)
		else:
			self.cur.execute(sentence)
		rows = self.cur.fetchall()
		return [x for x in rows]

	def insert(self, sentence, parameters=None):
		if parameters:
			self.cur.execute(sentence, parameters)
		else:
			self.cur.execute(sentence)
		self.con.commit()
		answ = self.cur.rowcount
		return answ

	def update(self, sentence, parameters=None):
		if parameters:
			self.cur.execute(sentence, parameters)
		else:
			self.cur.execute(sentence)
		self.con.commit()

	def delete(self, sentence, parameters=None):
		if parameters:
			self.cur.execute(sentence, parameters)
		else:
			self.cur.execute(sentence)
		answ = self.cur.rowcount
		self.con.commit()
		return answ
