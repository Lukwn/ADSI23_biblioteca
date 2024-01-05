from . import BaseTestClass
from bs4 import BeautifulSoup

class TestBueltatu(BaseTestClass):
    def test_liburu_bueltatu_ikusi(self):
        id = 2
        res = self.client.get(f'/bueltatu_aukeratu?user={id}')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(2, len(page.find('div', class_='list-group').find_all('div', class_='card')))

    def test_liburu_bueltatu(self):
        # Liburua erreserbatuta dago eta ez da bueltatu, beraz bueltatzean ez da errorerik egongo.
        user_id = 1
        book_id = 1
        sql_data = self.db.select(f"SELECT hasiera_data, bueltatze_data FROM Erreserba WHERE book_id = {book_id} AND user_id = {user_id} AND bueltatu_da = 0")
        hasiera_data = sql_data[0][0]
        bueltatze_data = sql_data[0][1]
        res = self.liburua_bueltatu(user_id, book_id)
        sql_test = self.db.select(f"SELECT * FROM Erreserba WHERE book_id = {book_id} AND user_id = {user_id} AND bueltatu_da = 1")[0]
        itxarotako_emaitza = (1, hasiera_data, 1, bueltatze_data, 1)
        self.assertEqual(itxarotako_emaitza, sql_test)
        self.assertEqual(200, res.status_code)
        # Espero den bezala orain liburua bueltatu da.

        # Bueltatuko den liburua jadanik bueltatu da, beraz bueltatzean ez da ezer gertatuko
        user_id = 1
        book_id = 0
        sql_data = self.db.select(
            f"SELECT hasiera_data, bueltatze_data FROM Erreserba WHERE book_id = {book_id} AND user_id = {user_id} AND bueltatu_da = 1")
        hasiera_data = sql_data[0][0]
        bueltatze_data = sql_data[0][1]
        res = self.liburua_bueltatu(user_id, book_id)
        sql_test = self.db.select(
            f"SELECT * FROM Erreserba WHERE book_id = {book_id} AND user_id = {user_id} AND bueltatu_da = 1")[0]
        itxarotako_emaitza = (1, hasiera_data, 0, bueltatze_data, 1)
        self.assertEqual(itxarotako_emaitza, sql_test)
        self.assertEqual(200, res.status_code)
        # Itxarotako emaitza eta lortutakoak berdinak dira, hau esan nahi du erreserbaren egoera ez dela aldatu

        # Existitzen ez den erabiltzaile bat liburu bat bueltatu nahi du (berdin da zein liburu den)
        user_id = 112312131
        book_id = 200
        res = self.liburua_bueltatu(user_id, book_id)
        sql_test = self.db.select(
            f"SELECT * FROM Erreserba WHERE book_id = {book_id} AND user_id = {user_id} AND bueltatu_da = 1")
        self.assertTrue(not sql_test)
        self.assertEqual(200, res.status_code)
        # Ez da emaitzarik lortzen, erreserba hau hasiera batean ez zelako existitzen

        # Existitzen ez den liburu bat bueltatzen saiatzen da norbaitek (berdin da nork)
        user_id = 1
        book_id = 20012313213121
        res = self.liburua_bueltatu(user_id, book_id)
        sql_test = self.db.select(
            f"SELECT * FROM Erreserba WHERE book_id = {book_id} AND user_id = {user_id} AND bueltatu_da = 1")
        self.assertTrue(not sql_test)
        self.assertEqual(200, res.status_code)
        # Ez da emaitzarik lortzen, erreserba hau hasiera batean ez zelako existitzen
