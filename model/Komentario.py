class Komentario:
    def __init__(self, id, gaia_id, user_id, txt):
        self.id = id
        self.gaia_id = gaia_id
        self.user_id = user_id
        self.txt = txt

    def id_da(self, id):
        if id == self.id:
            return True
        else:
            return False

    def get_txt(self):
        return self.txt