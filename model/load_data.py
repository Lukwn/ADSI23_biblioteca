import hashlib
import sqlite3
import json

salt = "library"


con = sqlite3.connect("../datos.db")
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
		name varchar(20),
		email varchar(30),
		password varchar(32)
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
		id integer primary key AUTOINCREMENT,
		gaia_id integer,
		txt varchar(250),
		FOREIGN KEY(gaia_id) REFERENCES Gaia(id)
	)
""")
### Insert users

with open('../usuarios.json', 'r') as f:
	usuarios = json.load(f)['usuarios']

for user in usuarios:
	dataBase_password = user['password'] + salt
	hashed = hashlib.md5(dataBase_password.encode())
	dataBase_password = hashed.hexdigest()
	cur.execute(f"""INSERT INTO User VALUES (NULL, '{user['nombres']}', '{user['email']}', '{dataBase_password}')""")
	con.commit()

#### Insert gaiak
with open('../gaiak.json', 'r') as f:
	gaiak = json.load(f)['gaiak']

for gaia in gaiak:
	cur.execute("INSERT INTO Gaia (id, izena) VALUES (?, ?)", (gaia['id'], gaia['izena']))
	"""for komentario in gaia['komentarioak']:
		cur.execute("INSERT INTO Komentario (gaia_id, txt) VALUES (?, ?)", (gaia['id'],komentario[2]))"""
	con.commit()

#### Insert komentarioak
with open('../komentarioak.json', 'r') as f:
	komentarioak = json.load(f)['komentarioak']

for k in komentarioak:
	cur.execute("INSERT INTO Komentario (id, gaia_id, txt) VALUES (?, ?, ?)", (k['id'], k['gaia_id'], k['txt']))
	con.commit()

#### Insert books
with open('../libros.tsv', 'r') as f:
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

