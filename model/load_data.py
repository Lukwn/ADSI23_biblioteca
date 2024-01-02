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
		username varchar(20),
		picture int,
		firstname varchar(20),
		lastname varchar(20),
		phone int,
		email varchar(30),
		password varchar(32),
		baimenak boolean,
		FOREIGN KEY (picture) REFERENCES Pictures(ID)
	)
""")

cur.execute("""
	CREATE TABLE Pictures(
		ID integer primary key ,
		link varchar(100)
	)
""")

cur.execute("""	
	CREATE TABLE Eskaera(
		EID1 integer,
		EID2 integer,
		baieztatuta boolean,
		PRIMARY KEY(EID1, EID2)
		FOREIGN KEY(EID1, EID2) REFERENCES User(id, id)
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
		user_id integer,
		txt varchar(250),
		respondiendo_a integer,
		respondiendo_a_txt varchar(250),
		FOREIGN KEY(gaia_id) REFERENCES Gaia(id),
		FOREIGN KEY(user_id) REFERENCES User(id),
		FOREIGN KEY(respondiendo_a) REFERENCES User(id)
	)
""")

cur.execute("""
	CREATE TABLE Erreseina(
		user_id  integer,
		book_id  integer,
		izarKop  integer,
		iruzkina varchar(1000),
		PRIMARY KEY (user_id, book_id),
		FOREIGN KEY (user_id) REFERENCES User (id),
		FOREIGN KEY (book_id) REFERENCES Book (id)
	)
""")

cur.execute("""
	CREATE TABLE Erreserba(
		user_id integer,
		hasiera_data date,
		book_id integer,
		bueltatze_data date,
		bueltatu_da integer,
		PRIMARY KEY (user_id, hasiera_data, book_id)
		FOREIGN KEY(user_id) REFERENCES User(id),
		FOREIGN KEY(book_id) REFERENCES Book(id)
	)
""")

### Insert users

## Insert eskaerak

with open('../eskaerak.json', 'r') as f:
	eskaeras = json.load(f)['eskaerak']

for eskaera in eskaeras:
	cur.execute(
		f"""INSERT INTO Eskaera VALUES ('{eskaera['id_1']}', '{eskaera['id_2']}', '{eskaera['baieztatuta']}')""")
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
	cur.execute(
		"INSERT INTO Komentario (id, gaia_id, user_id, txt, respondiendo_a, respondiendo_a_txt) VALUES (?, ?, ?, ?, ?, ?)",
		(k['id'], k['gaia_id'], k['user_id'], k['txt'], k['respondiendo_a'], k['respondiendo_a_txt']))
	con.commit()