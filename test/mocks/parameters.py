from utils.parameters import Parameters as RealParams

class Parameters(RealParams):

    def __init__(self):
        pass

    def setTypeOfDatabase(self, type):
        self.type = type

    def getTypeOfDatabase(self):
        return self.type