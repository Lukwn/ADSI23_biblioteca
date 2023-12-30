from model import Connection, Book, User, Gaia
from model.Komentario import Komentario
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
	def search_gaiak(self, izena="", limit=6, page=0):
		count = db.select("""
				SELECT count() 
				FROM Gaia
				WHERE izena LIKE ? 
		""", (f"%{izena}%",))[0][0]
		res = db.select("""
				SELECT *
				FROM Gaia
				WHERE izena LIKE ? 
				LIMIT ? OFFSET ?
		""", (f"%{izena}%", limit, limit*page))
		gaiak = [
			Gaia(g[0], g[1])
			for g in res
		]
		return gaiak, count

	def search_komentarioak(self, gaia_id="", limit=6, page=0):
		count = db.select("""
						SELECT count() 
						FROM Komentario
						WHERE gaia_id LIKE ? 
				""", (f"%{gaia_id}%",))[0][0]
		res = db.select("""
						SELECT *
						FROM Komentario
						WHERE gaia_id LIKE ? 
						LIMIT ? OFFSET ?
				""", (f"%{gaia_id}%", limit, limit * page))
		komentarioak = [
			Komentario(k[0], k[1], k[2], k[3])
			for k in res
		]
		return komentarioak, count
	def get_gaia(self, id):
		gaia = db.select("SELECT * from Gaia WHERE id = ?", (id,))
		return Gaia(gaia[0][0], gaia[0][1])
	def add_gaia(self, izena):
		db.insert("INSERT INTO Gaia (izena) VALUES (?)", (izena,))
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
