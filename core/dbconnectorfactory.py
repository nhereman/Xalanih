from utils.parameters import Parameters
from core.logger import Logger
from core.mysql.mysqlconnector import MysqlConnector
from core.xalanihexception import XalanihException
from core.constants import Constants

class DBConnectorFactory:
    @staticmethod
    def getConnection(params, logger):
        assert isinstance(params,Parameters)
        assert isinstance(logger, Logger)
        connector = None
        database_type = params.getTypeOfDatabase()
        logger.info("Connection to a {0} database".format(database_type))
        if(database_type == Constants.DB_MYSQL):
            connector = MysqlConnector(params, logger)
        if connector == None:
            raise XalanihException("DBConnectorFactory: This type of database" 
                                "is not managed :" + database_type + ".",
                                XalanihException.DB_TYPE_NOT_SUPPORTED)
        return connector.connect()
        