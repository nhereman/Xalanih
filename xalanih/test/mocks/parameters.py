from xalanih.utils.parameters import Parameters as RealParams

class Parameters(RealParams):

    def __init__(self):
        pass

    def setTypeOfDatabase(self, type):
        self.type = type

    def get_database_type(self):
        return self.type
