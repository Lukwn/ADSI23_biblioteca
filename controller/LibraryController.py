from model import Connection, Book, User, Erreseina, Gaia, Komentario, Erreserba
from flask import request
from model.tools import hash_password
from datetime import date,timedelta, datetime

db = Connection()


class LibraryController:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(LibraryController, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

##Liburuak eta katalogoa
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
        """, (f"%{title}%", f"%{author}%", limit, limit * page))
        books = [
            Book(b[0], b[1], b[2], b[3], b[4])
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
    	""", (f"%{izena}%", limit, limit * page))
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
    					SELECT u.username, k.*
    					FROM Komentario k, User u
    					WHERE gaia_id LIKE ? AND u.id = k.user_id
    					LIMIT ? OFFSET ? 
    			""", (f"%{gaia_id}%", limit, limit * page))
        komentarioak = [
            Komentario(k[0], k[1], k[2], k[3], k[4], k[5], k[6])
            for k in res
        ]
        return komentarioak, count

    def get_gaia(self, id):
        gaia = db.select("SELECT * from Gaia WHERE id = ?", (id,))
        if gaia:
            return Gaia(gaia[0][0], gaia[0][1])
        else:
            return None

    def add_gaia(self, izena):
        db.insert("INSERT INTO Gaia (izena) VALUES (?)", (izena,))

    def add_komentario(self, gaia_id, user_id, txt, respondiendo_a, respondiendo_a_txt):
        db.insert("INSERT INTO Komentario (gaia_id, user_id, txt, respondiendo_a, respondiendo_a_txt) VALUES (?, ?, ?, ?, ?)",
            (gaia_id, user_id, txt, respondiendo_a, respondiendo_a_txt,))
    def get_book(self, id):
        b = db.select("""
                        SELECT Book.*
                        FROM Book
                        WHERE Book.id = ?
                """, (id,))
        tupla = b[0]
        book = Book(tupla[0],tupla[1],tupla[2],tupla[3],tupla[4])
        return book

##Erabiltzailea sartzeko orduan
    def get_user(self, email, password):
        user = db.select("SELECT * from User WHERE email = ? AND password = ?", (email, hash_password(password)))
        if len(user) > 0:
            return User(user[0][0], user[0][1], user[0][2], user[0][4], user[0][5], user[0][6], user[0][7], user[0][8])
        else:
            return None
    def get_user_cookies(self, token, time):
        user = db.select(
            "SELECT u.* from User u, Session s WHERE u.id = s.user_id AND s.last_login = ? AND s.session_hash = ?",
            (time, token))
        if len(user) > 0:
            return User(user[0][0], user[0][1], user[0][2], user[0][4], user[0][5], user[0][6], user[0][7], user[0][8])
        else:
            return None

##Lagun sarea eta erabiltzelieen profila
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
        lagunak = [
            self.getUser(e[0]) if e[0] != id else self.getUser(e[1])
            for e in res
        ]
        pictures = [
            self.get_picture(pictureId.picture)
            for pictureId in lagunak
        ]
        return lagunak, pictures, count

    def getUser(self, id):
        username = db.select("SELECT * FROM User WHERE id = ?", (id,))
        if username:
            return User(username[0][0], username[0][1], username[0][2], username[0][4], username[0][5], username[0][6],
                        username[0][7], username[0][8])
        else:
            return None

    def getUserUsername(self, username):
        username = db.select("SELECT * FROM User WHERE username = ?", (username,))
        if username:
            return User(username[0][0], username[0][1], username[0][2], username[0][4], username[0][5], username[0][6],
                        username[0][7], username[0][8])
        else:
            return None

    def getUserMax(self):
        return db.select("SELECT MAX(id) FROM User")
    def get_picture(self, id):
        picture = db.select("SELECT link FROM Pictures WHERE ID = ?", (id,))
        if picture:
            return picture[0][0]
        else:
            return None

##Erabiltzileak bilatu
    def search_user(self, username="", limit=10, page=0):
        count = db.select("""
                              SELECT count()
                              FROM User
                              WHERE id!=? AND username LIKE ? 
                              AND User.id NOT IN (
                                SELECT Eskaera.EID1
                                FROM Eskaera
                                WHERE Eskaera.EID2 = ?
                                UNION
                                SELECT Eskaera.EID2
                                FROM Eskaera
                                WHERE Eskaera.EID1 = ?
                              )
                        """, (request.user.id, f"%{username}%", request.user.id, request.user.id))[0][0]
        res = db.select("""
                              SELECT *
                              FROM User
                              WHERE id!=? AND username LIKE ? 
                              AND User.id NOT IN (
                                SELECT Eskaera.EID1
                                FROM Eskaera
                                WHERE Eskaera.EID2 = ?
                                UNION
                                SELECT Eskaera.EID2
                                FROM Eskaera
                                WHERE Eskaera.EID1 = ?
                              )
                              LIMIT ? OFFSET ?
                        """, (request.user.id, f"%{username}%", request.user.id, request.user.id, limit, limit * page))
        users = [
            User(u[0], u[1], u[2], u[4], u[5], u[6], u[7], u[8])
            for u in res
        ]
        pictures = [
            self.get_picture(pictureId.picture)
            for pictureId in users
        ]
        return users, pictures, count

## Eskaerak
    def get_bidalitakoEskaerak(self, limit=5, page=0):
        count = db.select("""
                               SELECT count()
                               FROM Eskaera
                               WHERE EID1=? AND baieztatuta=0
                         """, (request.user.id,))[0][0]
        res = db.select("""
                               SELECT *
                               FROM Eskaera
                               WHERE EID1=? AND baieztatuta=0
                               LIMIT ? OFFSET ?
                         """, (request.user.id, limit, limit * page))
        bidali = [
            self.getUser(e[1])
            for e in res
        ]
        pictures = [
            self.get_picture(pictureId.picture)
            for pictureId in bidali
        ]
        return bidali, pictures, count

    def get_jasotakoEskaerak(self, limit=5, page=0):
        count = db.select("""
                               SELECT count()
                               FROM Eskaera
                               WHERE EID2=? AND baieztatuta=0
                         """, (request.user.id,))[0][0]
        res = db.select("""
                               SELECT *
                               FROM Eskaera
                               WHERE EID2=? AND baieztatuta=0
                               LIMIT ? OFFSET ?
                         """, (request.user.id, limit, limit * page))
        jaso = [
            self.getUser(e[0])
            for e in res
        ]
        pictures = [
            self.get_picture(pictureId.picture)
            for pictureId in jaso
        ]
        return jaso, pictures, count

    def onartuEskaera(self, id):
        db.update("UPDATE Eskaera SET baieztatuta=true WHERE EID1=? AND EID2=?", (id, request.user.id))

    def kenduUkatu(self, id):
        db.delete("DELETE FROM Eskaera WHERE (EID1=? AND EID2=?) OR (EID1=? AND EID2=?)", (id, request.user.id, request.user.id, id,))


    def gehituLagun(self, id):
        db.insert("INSERT INTO Eskaera VALUES (?,?,false)", (request.user.id, id))


    def erreseinatu_ahal_du(self, user_id=0, book_id=0):
        erreseina_ahal_du = False
        err = db.select("""
              SELECT e.*
              FROM Erreserba e, User u
              WHERE e.user_id= ? and e.book_id=? and e.bueltatu_da = 1
            """, (user_id,book_id))
        if err != []:
            erreseina_ahal_du= True
        print(erreseina_ahal_du)
        return erreseina_ahal_du

    def get_erreseinak(self, id=0, user_id=0, limit=20, page=0):
        # get erreseina guztiak erabiltzailearena izan ezik
        count = db.select("""
              SELECT count()
              FROM Erreseina e
              WHERE book_id = ? AND user_id != ?
            """, (id, user_id))[0][0]
        res = db.select("""
              SELECT u.username, e.*
              FROM Erreseina e, User u
              WHERE book_id = ? AND user_id != ? AND u.id = user_id
              LIMIT ? OFFSET ?
            """, (id, user_id, limit, limit * page))


        erreseinak = [
          Erreseina(err[0], err[1], err[2], err[3], err[4])
        for err in res
        ]
        return erreseinak, count


    def get_user_erreseina(self, id=0, user_id=0, limit=20, page=0):
        user_err = db.select("""
                     SELECT u.username, e.*
                     FROM Erreseina e, User u
                     WHERE book_id = ? AND user_id = ? AND u.id = user_id
                    LIMIT ? OFFSET ?
            """, (id, user_id, limit, limit * page))


        user_erreseina = [
            Erreseina(err[0], err[1], err[2], err[3], err[4])
            for err in user_err
        ]
        return user_erreseina

    def get_erreseinaGuztiak(self,id, limit=5, page=0):
        count = db.select("""
                      SELECT count()
                      FROM Erreseina
                      WHERE user_id = ?
                    """, (id,))[0][0]
        user_err = db.select("""
                              SELECT *
                              FROM Erreseina
                              WHERE user_id = ?
                              LIMIT ? OFFSET ?
                            """, (id, limit, limit*page))
        user_erreseina = [
            Erreseina('', err[0], err[1], err[2], err[3])
            for err in user_err
        ]
        books = [
            self.findBook(err[1])
            for err in user_err
        ]
        return user_erreseina, books, count

    def findBook(self, id):
        b = db.select("SELECT * FROM Book WHERE id=?", (id,))
        return Book(b[0][0], b[0][1], b[0][2], b[0][3], b[0][4])

    def add_erreseina(self, user_id, book_id, izarKop, iruzkina):
        db.insert("""
            INSERT INTO Erreseina (user_id, book_id, izarKop, iruzkina)
            VALUES (?, ?, ?, ?)
        """, (user_id, book_id, izarKop, iruzkina))


    def edit_erreseina(self, user_id, book_id, izarKop, iruzkina):
        db.update("""
            UPDATE Erreseina
            SET izarKop = ?, iruzkina = ?
            WHERE user_id = ? AND book_id = ?
        """, (izarKop, iruzkina, user_id, book_id))

    def search_history(self, id, title="", author="", limit=6, page=0):
        count = db.select("""
                SELECT count() 
                FROM Book b, Author a, Erreserba e
                WHERE b.author=a.id 
                    AND b.title LIKE ? 
                    AND a.name LIKE ?
                    AND e.user_id = ?
                    AND e.book_id = b.id
        """, (f"%{title}%", f"%{author}%", f"{id}"))[0][0]
        res = db.select("""
                SELECT b.*, e.hasiera_data, e.bueltatze_data, e.bueltatu_da
                FROM Book b, Author a, Erreserba e
                WHERE b.author=a.id 
                    AND b.title LIKE ? 
                    AND a.name LIKE ?
                    AND e.user_id = ?
                    AND e.book_id = b.id
                ORDER BY e.hasiera_data DESC
                LIMIT ? OFFSET ?
        """, (f"%{title}%", f"%{author}%", f"{id}", limit, limit * page))
        books = [
            [Book(b[0], b[1], b[2], b[3], b[4]), b[5], datetime.strptime(b[6], "%Y-%m-%d").date(), b[7]]
            for b in res
        ]
        return books, count

    def getErabiltzaileErreserba(self, id):
        res = db.select("""
                        SELECT e.*
                        FROM Erreserba e, User u
                        WHERE e.user_id = u.id
                            AND u.id = ?
                """, (f"{id}",))
        Erreserbak = [
            Erreserba(r[0], r[1], r[2], r[3], r[4])
            for r in res
        ]
        return Erreserbak

    def getLiburuErreserbaAktiboak(self, book_id):
        res = db.select("""
                        SELECT e.*
                        FROM Erreserba e, User u, Book b
                        WHERE e.book_id = b.id
                            AND e.bueltatu_da = 0
                            AND b.id = ?
                """, (f"{book_id}",))
        Erreserbak = [
            Erreserba(r[0], r[1], r[2], r[3], r[4])
            for r in res
        ]
        return Erreserbak

    def erreserbatu(self, id, book_id):
        ans = db.insert("""
                        INSERT INTO Erreserba VALUES (?, ?, ?, ?, ?)
                """, (f"{id}", f"{date.today()}", f"{book_id}", f"{date.today() + timedelta(days=30)}", f"{0}"))

    def search_erreserbatuta(self, user, title="", author="", limit=6, page=0):
        count = db.select("""
                SELECT count() 
                FROM Book b, Author a, Erreserba e
                WHERE b.author=a.id 
                    AND b.title LIKE ? 
                    AND a.name LIKE ?
                    AND e.user_id = ?
                    AND e.book_id = b.id
                    AND e.bueltatu_da = 0
        """, (f"%{title}%", f"%{author}%", f"{user}"))[0][0]
        res = db.select("""
                SELECT b.*, e.hasiera_data, e.bueltatze_data, e.bueltatu_da
                FROM Book b, Author a, Erreserba e
                WHERE b.author=a.id 
                    AND b.title LIKE ? 
                    AND a.name LIKE ?
                    AND e.user_id = ?
                    AND e.book_id = b.id
                    AND e.bueltatu_da = 0
                ORDER BY e.hasiera_data DESC
                LIMIT ? OFFSET ?
        """, (f"%{title}%", f"%{author}%", f"{user}", limit, limit * page))
        books = [
            [Book(b[0], b[1], b[2], b[3], b[4]), b[5], datetime.strptime(b[6], "%Y-%m-%d").date(), b[7]]
            for b in res
        ]
        return books, count

    def liburua_bueltatu(self, user, liburu_id):
        ans = db.update(""" 
                                UPDATE Erreserba SET bueltatu_da = 1 WHERE user_id = ? AND book_id = ?;
                        """, (f"{user}", f"{liburu_id}"))