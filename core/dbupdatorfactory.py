from utils.parameters import Parameters
from core.dbconnector import DBConnector
from core.dbchecker import DBChecker
from core.mysql.mysqlupdator import MysqlUpdator

class DBUpdatorFactory:
    @staticmethod
    def getUpdator(params, connector, checker):
        assert isinstance(params, Parameters)
        assert isinstance(connector, DBConnector)
        assert isinstance(checker, DBChecker)

        dbType = params.getTypeOfDatabase()

        if (dbType == "mysql"):
            return MysqlUpdator(params, connector, checker)

        raise Exception("The database type '" + dbType + 
                            "' is not supported.")