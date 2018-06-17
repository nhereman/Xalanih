from utils.parameters import Parameters
from core.dbconnector import DBConnector
from core.dbchecker import DBChecker
from core.mysql.mysqlcreator import MysqlCreator

class DBCreatorFactory:
    @staticmethod
    def getCreator(params, connector, checker):
        assert isinstance(params, Parameters)
        assert isinstance(connector, DBConnector)
        assert isinstance(checker, DBChecker)
        
        dbType = params.getTypeOfDatabase()

        if (dbType == "mysql"):
            return MysqlCreator(params, connector,checker)

        raise Exception("DBCreatorFactory-getCreator: The database type '" 
                        + dbType + "' is not supported.")
