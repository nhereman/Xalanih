from utils.parameters import Parameters
from core.dbconnector import DBConnector
from core.mysql.mysqlchecker import MysqlChecker

class DBCheckerFactory:
    @staticmethod
    def getChecker(params, connector):
        assert isinstance(params, Parameters)
        assert isinstance(connector, DBConnector)

        dbType = params.getTypeOfDatabase()

        if (dbType == "mysql"):
            return MysqlChecker(params, connector)

        raise Exception("DBCheckerFactory-getChecker: The database type '"
                            + dbType + "' is not supported.")