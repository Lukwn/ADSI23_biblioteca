from . import BaseTestClass
from model import Connection
from controller.LibraryController import LibraryController

db = Connection()
library = LibraryController()

class TestLagunSare(BaseTestClass):

    def testLagunakIkusi(self):
        self.login("james@gmail.com", "123456")
        db.select("DELETE FROM Eskaera WHERE EID1=1 OR EID2=1")
        #lagunik ez badago
        lagunak, pictures, count = library.search_lagunak(1)
        self.assertEqual(0, count)
        #lagun bat badu
        db.insert("INSERT INTO Eskaera VALUES (1, 3, true)")
        res = self.client.get('/lagunSarea')
        lagunak, pictures, count = library.search_lagunak(1)
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, count)
        #lagun bat baino gehiago badu
        db.insert("INSERT INTO Eskaera VALUES (1, 4, true)")
        lagunak, pictures, count = library.search_lagunak(1)
        self.assertEqual(2, count)
        #existitzen den lagun bat baldin badu
        db.insert("INSERT INTO Eskaera VALUES (1, 9999999, true)")
        res = self.client.get('/lagunSarea')
        self.assertEqual(500, res.status_code)

    def testLagunaKendu(self):
        self.login("james@gmail.com", "123456")
        user_id = 1
        db.select("DELETE FROM Eskaera WHERE EID1=1 OR EID2=1")
        #Lagunik ez baditu
        lagunak, pictures, count = library.search_lagunak(1)
        self.assertEqual(0, count)
        library.kenduUkatu(3, user_id) ##Id 3 duen laguna kendu

        db.insert("INSERT INTO Eskaera VALUES (1, 3, true)")
        db.insert("INSERT INTO Eskaera VALUES (1, 4, true)")
        db.insert("INSERT INTO Eskaera VALUES (1, 5, true)")
        db.insert("INSERT INTO Eskaera VALUES (1, 6, true)")
        lagunak, pictures, count = library.search_lagunak(1)
        self.assertEqual(4, count)
        ##Borrar al amigo
        library.kenduUkatu(6, user_id)
        lagunak, pictures, count = library.search_lagunak(1)
        self.assertEqual(3, count)
        ##Borrar amigo inexistente
        library.kenduUkatu(9999, user_id)
        lagunak, pictures, count = library.search_lagunak(1)
        self.assertEqual(3, count)
        res = self.client.get('/lagunSarea')
        self.assertEqual(200, res.status_code)


    def testLagunEskaeraBidali(self):
        self.login("james@gmail.com", "123456")
        user_id = 1
        db.select("DELETE FROM Eskaera WHERE EID1=1 OR EID2=1")
        lagunak, pictures, count = library.get_bidalitakoEskaerak(1)
        self.assertEqual(0, count)

        ##Erabiltzaile bati eskaera bidali
        library.gehituLagun(3, user_id)
        lagunak, pictures, count = library.get_bidalitakoEskaerak(1)
        self.assertEqual(1, count)

        ##Erabiltzaile inexistente bati eskaera bidali
        library.gehituLagun(9999, user_id)
        self.assertEqual(2, db.select("SELECT count() FROM Eskaera WHERE EID1=1 OR EID2=1")[0][0])
        res = self.client.get('/eskaerak')
        self.assertEqual(500, res.status_code)

    def testOnartuEskaera(self):
        self.login("james@gmail.com", "123456")
        user_id = 1
        db.select("DELETE FROM Eskaera WHERE EID1=1 OR EID2=1")
        lagunak, pictures, count = library.search_lagunak(1)
        self.assertEqual(0, count)

        db.insert("INSERT INTO Eskaera VALUES (3, 1, false)")
        db.insert("INSERT INTO Eskaera VALUES (4, 1, false)")

        ##Eskaera onartu
        library.onartuEskaera(3, user_id)
        lagunak, pictures, count = library.search_lagunak(1)
        self.assertEqual(1, count)

        library.onartuEskaera(4, user_id)
        lagunak, pictures, count = library.search_lagunak(1)
        self.assertEqual(2, count)

        ##Eskaera inexistente bat onartu
        library.onartuEskaera(5, user_id)
        lagunak, pictures, count = library.search_lagunak(1)
        self.assertEqual(2, count)

        ##Erabiltzaile inexistente baten lagun eskaera onartu
        db.insert("INSERT INTO Eskaera VALUES (9999, 1, false)")
        library.onartuEskaera(9999, user_id)
        res = self.client.get('/lagunSarea')
        self.assertEqual(500, res.status_code)

    def testUkatuEskaera(self):
        self.login("james@gmail.com", "123456")
        user_id = 1
        db.select("DELETE FROM Eskaera WHERE EID1=1 OR EID2=1")

        db.insert("INSERT INTO Eskaera VALUES (3, 1, false)")
        db.insert("INSERT INTO Eskaera VALUES (4, 1, false)")
        db.insert("INSERT INTO Eskaera VALUES (5, 1, false)")

        lagunak, pictures, count = library.get_jasotakoEskaerak(1)
        self.assertEqual(3, count)

        ##Erabiltzaile baten eskaera ukatu
        library.kenduUkatu(3, user_id)
        lagunak, pictures, count = library.get_jasotakoEskaerak(1)
        self.assertEqual(2, count)
        library.kenduUkatu(4, user_id)
        lagunak, pictures, count = library.get_jasotakoEskaerak(1)
        self.assertEqual(1, count)

        ##Erabiltzaile inexistente baten eskaera ukatu
        db.insert("INSERT INTO Eskaera VALUES (9999, 1, false)")
        library.kenduUkatu(9999, user_id)
        lagunak, pictures, count = library.get_jasotakoEskaerak(1)
        self.assertEqual(1, count)

        ##Eskaera inexistente bat ukatu
        library.kenduUkatu(6, user_id)
        lagunak, pictures, count = library.get_jasotakoEskaerak(1)
        self.assertEqual(1, count)


    def testEzabatuEskaera(self):
        self.login("james@gmail.com", "123456")
        user_id = 1
        db.select("DELETE FROM Eskaera WHERE EID1=1 OR EID2=1")

        db.insert("INSERT INTO Eskaera VALUES (1, 3, false)")
        db.insert("INSERT INTO Eskaera VALUES (1, 4, false)")
        db.insert("INSERT INTO Eskaera VALUES (1, 5, false)")

        lagunak, pictures, count = library.get_bidalitakoEskaerak(1)
        self.assertEqual(3, count)

        ##Erabiltzaile bati bidalitako eskaera ezabatu
        library.kenduUkatu(3, user_id)
        lagunak, pictures, count = library.get_bidalitakoEskaerak(1)
        self.assertEqual(2, count)
        library.kenduUkatu(4, user_id)
        lagunak, pictures, count = library.get_bidalitakoEskaerak(1)
        self.assertEqual(1, count)

        ##Erabiltzaile inexistente bati bidalitako eskaera ezabatu
        db.insert("INSERT INTO Eskaera VALUES (1, 9999, false)")
        library.kenduUkatu(9999, user_id)
        lagunak, pictures, count = library.get_bidalitakoEskaerak(1)
        self.assertEqual(1, count)

        ##Eskaera inexistente bat ezabatu
        library.kenduUkatu(6, user_id)
        lagunak, pictures, count = library.get_bidalitakoEskaerak(1)
        self.assertEqual(1, count)

    def testProfilaIkusi(self):
        self.login("james@gmail.com", "123456")
        user_id = 1

        db.delete('DELETE FROM Erreseina WHERE user_id = 1')
        db.delete('DELETE FROM Erreserba WHERE user_id = 1')

        erreseinak, books, count = library.get_erreseinaGuztiak(1)
        self.assertEqual(0, count)
        erreserbak, books, count = library.getErabiltzaileErreserbaAktiboak(1)
        self.assertEqual(0, count)

        ##Nire profila ikusi (erreseina eta erreserba gabe)
        res = self.client.get('/usr-Jamesito')
        self.assertEqual(200, res.status_code)

        #Erreseinak baditu
        library.add_erreseina(user_id, 1, 7, 'Ondo')
        erreseinak, books, count = library.get_erreseinaGuztiak(1)
        self.assertEqual(1, count)
        library.add_erreseina(user_id, 2, 3, 'Txarto')
        erreseinak, books, count = library.get_erreseinaGuztiak(1)
        self.assertEqual(2, count)

        res = self.client.get('/usr-Jamesito')
        self.assertEqual(200, res.status_code)

        db.delete('DELETE FROM Erreseina WHERE user_id = 1')
        ##Erreserabak baditu
        library.erreserbatu(user_id, 2)
        erreserbak, books, count = library.getErabiltzaileErreserbaAktiboak(1)
        self.assertEqual(1, count)
        library.erreserbatu(user_id, 3)
        erreserbak, books, count = library.getErabiltzaileErreserbaAktiboak(1)
        self.assertEqual(2, count)

        res = self.client.get('/usr-Jamesito')
        self.assertEqual(200, res.status_code)

        db.delete('DELETE FROM Erreserba WHERE user_id = 1')

        ##Erreseinak eta erreserbak baditu
        library.add_erreseina(user_id, 1, 7, 'Ondo')
        erreseinak, books, count = library.get_erreseinaGuztiak(1)
        self.assertEqual(1, count)
        library.add_erreseina(user_id, 2, 3, 'Txarto')
        erreseinak, books, count = library.get_erreseinaGuztiak(1)
        self.assertEqual(2, count)

        library.erreserbatu(user_id, 2)
        erreserbak, books, count = library.getErabiltzaileErreserbaAktiboak(1)
        self.assertEqual(1, count)
        library.erreserbatu(user_id, 3)
        erreserbak, books, count = library.getErabiltzaileErreserbaAktiboak(1)
        self.assertEqual(2, count)

        res = self.client.get('/usr-Jamesito')
        self.assertEqual(200, res.status_code)

        #Beste erabiltzaile baten profila ikusi
        res = self.client.get('/usr-Pablito')
        self.assertEqual(200, res.status_code)