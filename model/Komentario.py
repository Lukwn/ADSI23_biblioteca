class Komentario:
    def __init__(self, username, id, gaia_id, user_id, txt, respondiendo_a, respondiendo_a_txt):
        self.username = username
        self.id = id
        self.gaia_id = gaia_id
        self.user_id = user_id
        self.txt = txt
        self.respondiendo_a = respondiendo_a
        self.respondiendo_a_txt = respondiendo_a_txt

    def id_da(self, id):
        if id == self.id:
            return True
        else:
            return False

    def get_txt(self):
        return self.txt