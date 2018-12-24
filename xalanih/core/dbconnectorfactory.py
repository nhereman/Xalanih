from xalanih.core.parameters import Parameters
from xalanih.core.logger import Logger
from xalanih.core.mysql.mysqlconnector import MysqlConnector
from xalanih.core.postgresql.postgresqlconnector import PostgreSQLConnector
from xalanih.core.xalanihexception import XalanihException
from xalanih.core.constants import Constants


class DBConnectorFactory:
    @staticmethod
    def get_connection(params, logger):
        """
        Get the connection object associated to the database.
        Argument:
        - params: Parameters object. Required for the connectors
                  and the database type.
        - logger: The logger.
        returns: A connection object
        """
        assert isinstance(params, Parameters)
        assert isinstance(logger, Logger)
        connector = None
        database_type = params.get_database_type()
        logger.info("Connection to a {0} database".format(database_type))
        if database_type == Constants.DB_MYSQL:
            connector = MysqlConnector(params, logger)
        elif database_type == Constants.DB_POSTGRESQL:
            connector = PostgreSQLConnector(params, logger)
        if connector is None:
            raise XalanihException("DBConnectorFactory: This type of database" 
                                   "is not managed :" + database_type + ".",
                                   XalanihException.DB_TYPE_NOT_SUPPORTED)
        return connector.connect()

