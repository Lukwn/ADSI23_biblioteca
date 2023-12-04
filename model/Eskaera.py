class Eskaera:
    def __new__(cls, *args, **kwargs):
        EID1 = args[1]
        EID2 = args[2]
        onartua = False

    def getLagunID(self,nireID):
        if (nireID == self.EID1):
            return self.EID2
        else:
            return self.EID1

    def onartu(self):
        self.onartua = True