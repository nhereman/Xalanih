from utils.parameters import Parameters
from core.mysql.mysqlconnector import MysqlConnector

class DBConnectorFactory:
    @staticmethod
    def getConnector(params):
        assert isinstance(params,Parameters)
        dbType = params.getTypeOfDatabase()
        if(dbType == "mysql"):
            return MysqlConnector(params)
        raise Exception("DBConnectorFactory: This type of database is not managed :" + dbType + ".")
        