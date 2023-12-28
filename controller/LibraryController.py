from model import Connection, Book, User
from model.tools import hash_password

db = Connection()

class LibraryController:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(LibraryController, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance


	def search_books(self, title="", author="", limit=6, page=0):
		count = db.select("""
				SELECT count() 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
		""", (f"%{title}%", f"%{author}%"))[0][0]
		res = db.select("""
				SELECT b.* 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
				LIMIT ? OFFSET ?
		""", (f"%{title}%", f"%{author}%", limit, limit*page))
		books = [
			Book(b[0],b[1],b[2],b[3],b[4])
			for b in res
		]
		return books, count

	def search_lagunak(self, id=0, limit=10, page=0):
		count = db.select("""
						SELECT count() 
						FROM Eskaera 
						WHERE (EID1=? OR EID2=?) AND baieztatuta=1
				""", (id, id))[0][0]
		res = db.select("""
						SELECT * 
						FROM Eskaera 
						WHERE (EID1=? OR EID2=?) AND baieztatuta=1
						LIMIT ? OFFSET ?
				""", (id, id, limit, limit * page))
		eskaerak = [
			self.getUsername(e[0]) if e[0]!=id  else self.getUsername(e[1])
			for e in res
		]
		return eskaerak, count

	def getUsername(self, id):
		username = db.select("SELECT name FROM User WHERE id = ?", (id,))
		if username:
			return username[0][0]
		else:
			return None

	def get_user(self, email, password):
		user = db.select("SELECT * from User WHERE email = ? AND password = ?", (email, hash_password(password)))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2])
		else:
			return None

	def get_user_cookies(self, token, time):
		user = db.select("SELECT u.* from User u, Session s WHERE u.id = s.user_id AND s.last_login = ? AND s.session_hash = ?", (time, token))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2])
		else:
			return None





'''
	def search_gaiak(self, title="", limit=6, page=0):
		count = db.select("""
				SELECT count() 
				FROM GAIA G, 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
		""", (f"%{title}%", f"%{author}%"))[0][0]
		res = db.select("""
				SELECT b.* 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
				LIMIT ? OFFSET ?
		""", (f"%{title}%", f"%{author}%", limit, limit*page))
		books = [
			Book(b[0],b[1],b[2],b[3],b[4])
			for b in res
		]
		return books, count
		
'''