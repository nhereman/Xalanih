from utils.parameters import Parameters
from core.mysql.mysqlconnector import MysqlConnector

class DBConnectorFactory:
    @staticmethod
    def getConnection(params):
        assert isinstance(params,Parameters)
        connector = None
        dbType = params.getTypeOfDatabase()
        if(dbType == "mysql"):
            connector = MysqlConnector(params)
        if connector == None:
            raise Exception("DBConnectorFactory: This type of database" 
                                "is not managed :" + dbType + ".")
        return connector.connect()
        