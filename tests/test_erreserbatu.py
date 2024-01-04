from . import BaseTestClass
from datetime import date,timedelta

class TestErreserbatu(BaseTestClass):
    def test_liburu_erreserbatu(self):
        # Erreserba egiterakoak liburu hori ez dago erreserbatuta eta erreserbatuko duen erabiltzailea ez du epez kanpoko.
        book_id = 100
        self.login("jhon@gmail.com", "123")
        res = self.liburua_erreserbatu(book_id)
        sql_test = self.db.select(f"SELECT * FROM Erreserba WHERE user_id = 2 AND book_id = {book_id} AND bueltatu_da = 0")[0]
        itxarotako_emaitza = (2, date.today().strftime("%Y-%m-%d"), 100, (date.today() + timedelta(days=30)).strftime("%Y-%m-%d"), 0)
        self.assertEqual(200, res.status_code)
        self.assertTupleEqual(sql_test, itxarotako_emaitza)
        # Erreserba espero den bezala burutzen da.

        # Erreserba egiterakoan ez dago erabiltzailerik login-a egin duena.
        self.logout()
        book_id = 101
        res = self.liburua_erreserbatu(book_id)
        sql_test = self.db.select(f"SELECT * FROM Erreserba WHERE book_id = {book_id} AND bueltatu_da = 0")
        self.assertEqual(302, res.status_code)
        self.assertEqual(res.location, "/login")
        self.assertTrue(not sql_test)
        # Web orrialdea ez du errorerik emango, baina ez da libururik erreserbatuko eta birbideratuko gaitu (302)

        # Erreserba egiterakoak liburu hori erreserbatuta dago eta erreserbatuko duen erabiltzailea ez du epez kanpoko erreserbarik
        book_id = 1
        self.login("jhon@gmail.com", "123")
        res = self.liburua_erreserbatu(book_id)
        sql_test = self.db.select(f"SELECT * FROM Erreserba WHERE user_id = 2 AND book_id = {book_id} AND bueltatu_da = 0")
        self.assertEqual(200, res.status_code)
        self.assertTrue(not sql_test)
        # Espero den bezala erreserba ez da egiten

        # Erreserba egiterakoak liburua ez dago erreserbatuta baina erabiltzaileak epez kanpoko erreserba bat du
        self.logout()
        book_id = 102
        self.login("james@gmail.com", "123456")
        res = self.liburua_erreserbatu(book_id)
        sql_test = self.db.select(f"SELECT * FROM Erreserba WHERE user_id = 1 AND book_id = {book_id} AND bueltatu_da = 0")
        self.assertEqual(200, res.status_code)
        self.assertTrue(not sql_test)

        # Erreserba egiterakoak liburua ez da existitzen
        book_id = 1020121
        self.login("john@gmail.com", "123")
        res = self.liburua_erreserbatu(book_id)
        self.db.select(f"SELECT * FROM Erreserba WHERE user_id = 2 AND book_id = {book_id} AND bueltatu_da = 0")
        self.assertEqual(200, res.status_code)
        self.assertTrue(not sql_test)
