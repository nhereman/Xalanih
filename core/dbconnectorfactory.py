from utils.parameters import Parameters
from core.mysql.mysqlconnector import MysqlConnector
from core.xalanihexception import XalanihException

class DBConnectorFactory:
    @staticmethod
    def getConnection(params):
        assert isinstance(params,Parameters)
        connector = None
        dbType = params.getTypeOfDatabase()
        if(dbType == "mysql"):
            connector = MysqlConnector(params)
        if connector == None:
            raise XalanihException("DBConnectorFactory: This type of database" 
                                "is not managed :" + dbType + ".",
                                XalanihException.DB_TYPE_NOT_SUPPORTED)
        return connector.connect()
        