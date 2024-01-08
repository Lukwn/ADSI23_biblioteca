import json
import random
from . import BaseTestClass
from bs4 import BeautifulSoup


class TestCatalogo(BaseTestClass):

    def test_erreseinak_ikusi(self):
        # request success
        res = self.client.get('/book?id=1')
        self.assertEqual(200, res.status_code)
        #erreseinen atala behar den bezala agertzen den konprobatu
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(1, len(page.find('div', class_='userCard').find_all('div', class_='card')))

    def test_gehitu_erreseina(self):
        self.login('jhon@gmail.com', '123')
        book_id = 155
        izarKop = 5
        iruzkina = 'Prueba'
        res = self.add_erreseina(book_id=book_id, izarKop=izarKop, iruzkina=iruzkina)
        sql_test = self.db.select(
            f"SELECT * FROM Erreseina WHERE izarKop=izarKop AND iruzkina=iruzkina AND user_id=2 AND book_id={book_id}")[
            0]
        itxarotako_emaitza = (2, book_id, izarKop, iruzkina) #2=jhon id
        self.assertTupleEqual(sql_test, itxarotako_emaitza)


    def test_gehitu_erreseina_hutsa(self):
        self.login('jhon@gmail.com', '123')
        book_id = 200
        izarKop = ''
        iruzkina = ''
        res = self.add_erreseina(book_id=book_id, izarKop=izarKop, iruzkina=iruzkina)
        sql_test = self.db.select(
            f"SELECT * FROM Erreseina WHERE izarKop=izarKop AND iruzkina=iruzkina AND user_id=2 AND book_id={book_id}")
        self.assertEqual(200, res.status_code)  # ez du errore kodea eman
        self.assertTrue(not sql_test)  # ez da erantzunik aurkitu, hau da, ez da datu basean gehitu


    def test_gehitu_erreseina_txarto(self):
        self.login('jhon@gmail.com', '123')
        book_id = 250
        #izar kopuru ez egokia
        izarKop = 50
        #1000 karaktere baino gehiagoko testua
        iruzkina = 'La luz del amanecer se filtraba tímidamente a través de las cortinas entreabiertas, pintando el dormitorio con tonalidades cálidas. Ana despertó con la suave caricia del sol en su rostro y se estiró lentamente, disfrutando de esos instantes preciosos antes de que el bullicio del día la envolviera por completo. El aroma del café recién hecho flotaba en el aire, impregnando la cocina con su fragancia reconfortante. Mientras saboreaba cada sorbo, Ana repasaba mentalmente la agenda del día. Reuniones, tareas pendientes y proyectos creativos llenaban su jornada, pero también guardaba espacio para esos pequeños placeres que hacían la vida más rica. Decidió tomar un breve paseo por el parque cercano antes de sumergirse en las responsabilidades laborales. El crujir de las hojas bajo sus pies y el canto de los pájaros creaban una sinfonía natural que la transportaba a un estado de serenidad. En medio de la naturaleza, Ana encontraba inspiración y claridad mental. A lo largo del día, enfrentó desafíos y celebró pequeños triunfos. La interacción con colegas y la resolución creativa de problemas la mantenían en constante movimiento. Al caer la tarde, se retiró a su refugio hogareño, donde la luz tenue y el silencio la invitaban a la reflexión. En el crepúsculo, Ana se sumergió en la lectura de un libro que había estado esperando. Las palabras fluían como un río, transportándola a mundos lejanos y expandiendo su imaginación. La lectura, para ella, era un escape y una fuente inagotable de aprendizaje. Antes de dormir, Ana se asomó a la ventana y contempló las estrellas en el cielo nocturno. Cada destello parecía contar historias milenarias, recordándole la vastedad del universo. Con gratitud en el corazón, se deslizó entre las sábanas, lista para dejarse llevar por los sueños. Así transcurrió un día en la vida de Ana, una jornada equilibrada entre el trabajo y el disfrute, entre la eficiencia y la contemplación. En cada momento, buscaba la armonía y la plenitud, recordando que la vida se compone de instantes fugaces que merecen ser apreciados'
        res = self.add_erreseina(book_id=book_id, izarKop=izarKop, iruzkina=iruzkina)
        sql_test = self.db.select(
            f"SELECT * FROM Erreseina WHERE izarKop=izarKop AND iruzkina=iruzkina AND user_id=2 AND book_id={book_id}")
        self.assertEqual(200, res.status_code) #ez du errore kodea eman
        self.assertTrue(not sql_test) #ez da erantzunik aurkitu, hau da, ez da datu basean gehitu

    def test_editatu_erreseina(self):
        self.login('jhon@gmail.com', '123')
        book_id = 150
        izarKop = 7
        iruzkina = 'aldaketa'
        res = self.edit_erreseina(book_id=book_id, izarKop=izarKop, iruzkina=iruzkina)
        sql_test = self.db.select(
            f"SELECT * FROM Erreseina WHERE izarKop=izarKop AND iruzkina=iruzkina AND user_id=2 AND book_id={book_id}")[0]
        itxarotako_emaitza = (2, 150, 7, 'aldaketa')  # jhon-en id-a, liburu id-a, izarKop, testua
        self.assertTupleEqual(sql_test, itxarotako_emaitza)






