import hashlib
import sqlite3
import json

salt = "library"

def __init__():
	con = sqlite3.connect("datos.db")
	cur = con.cursor()

	### Create tables
	cur.execute("""
		CREATE TABLE Author(
			id integer primary key AUTOINCREMENT,
			name varchar(40)
		)
	""")

	cur.execute("""
		CREATE TABLE Book(
			id integer primary key AUTOINCREMENT,
			title varchar(50),
			author integer,
			cover varchar(50),
			description TEXT,
			FOREIGN KEY(author) REFERENCES Author(id)
		)
	""")

	cur.execute("""
		CREATE TABLE User(
			id integer primary key AUTOINCREMENT,
			username varchar(20),
			picture int,
			firstname varchar(20),
			lastname varchar(20),
			phone int,
			email varchar(30),
			password varchar(32)
		)
	""")

	cur.execute("""
		CREATE TABLE Pictures(
			ID integer,
			link varchar(100)
		)
	""")

	cur.execute("""
		CREATE TABLE Eskaera(
			EID1 integer,
			EID2 integer,
			baieztatuta boolean,
			FOREIGN KEY(EID1, EID2) REFERENCES User(id)
		)
	""")

	cur.execute("""
		CREATE TABLE Session(
			session_hash varchar(32) primary key,
			user_id integer,
			last_login float,
			FOREIGN KEY(user_id) REFERENCES User(id)
		)
	""")

	cur.execute("""
		CREATE TABLE Gaia(
			id integer primary key AUTOINCREMENT,
	    	izena VARCHAR(50)
	    )
	""")

	cur.execute("""
		CREATE TABLE Komentario(
			user_id integer,
			gaia_id integer,
			txt varchar(250)
			FOREIGN KEY(gaia_id) REFERENCES Gaia(id)
		)
	""")

	### Insert users

	with open('usuarios.json', 'r') as f:
		usuarios = json.load(f)['usuarios']

	for user in usuarios:
		dataBase_password = user['password'] + salt
		hashed = hashlib.md5(dataBase_password.encode())
		dataBase_password = hashed.hexdigest()
		cur.execute(
			f"""INSERT INTO User VALUES (NULL, '{user['nombres']}', '{user['email']}', '{dataBase_password}')""")
		con.commit()

	## Insert eskaerak

	with open('eskaerak.json', 'r') as f:
		eskaeras = json.load(f)['eskaerak']

	for eskaera in eskaeras:
		cur.execute(
			f"""INSERT INTO Eskaera VALUES ('{eskaera['id_1']}', '{eskaera['id_2']}', '{eskaera['baieztatuta']}')""")
		con.commit()

	#### Insert books
	with open('libros.tsv', 'r') as f:
		libros = [x.split("\t") for x in f.readlines()]

	for author, title, cover, description in libros:
		res = cur.execute(f"SELECT id FROM Author WHERE name=\"{author}\"")
		if res.rowcount == -1:
			cur.execute(f"""INSERT INTO Author VALUES (NULL, \"{author}\")""")
			con.commit()
			res = cur.execute(f"SELECT id FROM Author WHERE name=\"{author}\"")
		author_id = res.fetchone()[0]

		cur.execute("INSERT INTO Book VALUES (NULL, ?, ?, ?, ?)",
					(title, author_id, cover, description.strip()))

		con.commit()