from model import Connection, Book, User, Erreserba
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

    def get_user(self, email, password):
        user = db.select("SELECT * from User WHERE email = ? AND password = ?", (email, hash_password(password)))
        if len(user) > 0:
            return User(user[0][0], user[0][1], user[0][2])
        else:
            return None

    def get_user_cookies(self, token, time):
        user = db.select(
            "SELECT u.* from User u, Session s WHERE u.id = s.user_id AND s.last_login = ? AND s.session_hash = ?",
            (time, token))
        if len(user) > 0:
            return User(user[0][0], user[0][1], user[0][2])
        else:
            return None

    def get_book(self, id):
        b = db.select("""
                        SELECT Book.*
                        FROM Book
                        WHERE Book.id = ?
                """, (id,))
        tupla = b[0]
        book = Book(tupla[0],tupla[1],tupla[2],tupla[3],tupla[4])
        return book

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
                """, (f"{id}", ))
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
                """, (f"{book_id}", ))
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
