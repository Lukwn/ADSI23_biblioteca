from . import BaseTestClass
from bs4 import BeautifulSoup

class TestAdmin(BaseTestClass):

    def test_email_erabilia(self):
        res = self.login('james@gmail.com', '123456')
        # james@gmail.com duen kontu bat jadanik dago
        response = self.client.post('/erabSartu', data={'username': 'Paco234', 'email': 'james@gmail.com'})
        page = BeautifulSoup(response.data, features="html.parser")
        print(page)
        self.assertIn("Mesedez kontuari beste email bat jarri", page.text)

    def test_username_erabilia(self):
        res = self.login('james@gmail.com', '123456')
        # Jamesito izena duen kontu bat jadanik dago
        response = self.client.post('/erabSartu', data={'username': 'Jamesito', 'email': 'noesta@gmail.com'})
        page = BeautifulSoup(response.data, features="html.parser")
        print(page)
        self.assertIn("Mesedez kontuari beste izen bat jarri", page.text)

    def test_erabiltzaile_berria(self):
        res = self.login('james@gmail.com', '123456')
        dago = self.db.select("SELECT COUNT(*) FROM User WHERE username = ?", ("Proba",))
        self.assertEqual(dago[0][0], 0)
        # html-an zihurtatzen da sartutako karaktere kopurua ez dela onartzen den baino handiagoa eta email-a email bat izatea eta telefonoa 9 zenbaki edukitzea eta kanpo guztiak beteta egotea
        self.client.post('/erabSartu', data={'username': 'Proba', 'email': 'noesta@gmail.com','password': '123456', 'firstname':'Proba', 'lastname':'proba proba','picture':'5','phone':'634100435','baimenak':'on'})
        dago = self.db.select("SELECT COUNT(*) FROM User WHERE username = ?", ("Proba",))
        self.assertEqual(dago[0][0], 1)
        user=self.db.select("SELECT * FROM User WHERE username = ?", ("Proba",))
        print(user)
        self.db.delete("DELETE FROM User WHERE username = ?", ('Proba',))
