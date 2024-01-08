from . import BaseTestClass
from bs4 import BeautifulSoup

class TestAdmin(BaseTestClass):

    def test_borratu_erabiltzailea(self):
        self.login('james@gmail.com', '123456')
        self.client.post('/erabSartu', data={'username': 'Proba', 'email': 'noesta@gmail.com', 'password': '123456',
                                             'firstname': 'Proba', 'lastname': 'proba proba', 'picture': '5',
                                             'phone': '634100435', 'baimenak': 'on'})
        dago = self.db.select("SELECT COUNT(*) FROM User WHERE username = ?", ("Proba",))
        self.assertEqual(dago[0][0], 1)
        self.client.post('/erabEzab', data={'erabiltzailea': 'Proba', 'submit_button': 'sartu'})
        dago = self.db.select("SELECT COUNT(*) FROM User WHERE username = ?", ("Proba",))
        self.assertEqual(dago[0][0], 0)

    def test_bilatu_erabiltzaileak(self):
        self.login('james@gmail.com', '123456')
        self.client.post('/erabSartu', data={'username': 'Proba', 'email': 'noesta@gmail.com', 'password': '123456',
                                             'firstname': 'Proba', 'lastname': 'proba proba', 'picture': '5',
                                             'phone': '634100435', 'baimenak': 'on'})


        res = self.client.post('/erabEzab', data={'username': 'Proba', 'email': 'noesta@gmail.com', 'submit_button': 'search'})
        self.assertEqual(200, res.status_code)
        soup = BeautifulSoup(res.data, 'html.parser')
        #bilatu zenbat erabiltzaile agertzen diren (bakarrik bat agertu behar da)
        select_element = soup.find('select', id='erabiltzailea')
        users = len(select_element.find_all('option'))
        self.assertEqual(1, users)
        self.db.delete("DELETE FROM User WHERE username = ?", ('Proba',))



    def test_bilaketa_hutsa(self):
        self.login('james@gmail.com', '123456')
        self.client.post('/erabSartu', data={'username': 'Proba', 'email': 'noesta@gmail.com', 'password': '123456',
                                             'firstname': 'Proba', 'lastname': 'proba proba', 'picture': '5',
                                             'phone': '634100435', 'baimenak': 'on'})

        res = self.client.post('/erabEzab',
                               data={'username': 'EzDagoIzenHau', 'email': '', 'submit_button': 'search'})
        self.assertEqual(200, res.status_code)
        soup = BeautifulSoup(res.data, 'html.parser')
        # bilatu zenbat erabiltzaile agertzen diren (bakarrik bat agertu behar da)
        select_element = soup.find('select', id='erabiltzailea')
        users = len(select_element.find_all('option'))
        self.assertEqual(0, users)
        self.db.delete("DELETE FROM User WHERE username = ?", ('Proba',))


    def test_bilaketa_parametrorik_gabe(self):
        self.login('james@gmail.com', '123456')
        self.client.post('/erabSartu', data={'username': 'Proba', 'email': 'noesta@gmail.com', 'password': '123456',
                                             'firstname': 'Proba', 'lastname': 'proba proba', 'picture': '5',
                                             'phone': '634100435', 'baimenak': 'on'})

        res = self.client.post('/erabEzab',
                               data={'username': '', 'email': '', 'submit_button': 'search'})
        self.assertEqual(200, res.status_code)
        soup = BeautifulSoup(res.data, 'html.parser')
        # bilatu zenbat erabiltzaile agertzen diren (bakarrik bat agertu behar da)
        select_element = soup.find('select', id='erabiltzailea')
        users = len(select_element.find_all('option'))
        erab_kop = self.db.select("SELECT COUNT(*) FROM User")
        self.assertEqual(users, erab_kop[0][0])
        self.db.delete("DELETE FROM User WHERE username = ?", ('Proba',))