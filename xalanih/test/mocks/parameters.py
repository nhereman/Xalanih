from xalanih.core.parameters import Parameters as RealParams
from xalanih.core.connectioninfo import ConnectionInfo


class Parameters(RealParams):

    def __init__(self):
        self.type = None

    def set_type_of_database(self, db_type):
        self.type = db_type

    def get_database_type(self):
        return self.type

    def get_connection_info(self):
        return ConnectionInfo()

    def get_socket(self):
        return ""
