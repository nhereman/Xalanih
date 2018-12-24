from xalanih.core.parameters import Parameters
from xalanih.core.mysql.mysqlrequesthandler import MysqlRequestHandler
from xalanih.core.postgresql.postgresqlrequesthandler import PostgreSQLRequestHandler
from xalanih.core.xalanihexception import XalanihException
from xalanih.core.constants import Constants


class RequestHandlerFactory:
    @staticmethod
    def get_request_handler(params):
        """
        Get the RequestHandler object linked to the type of database.
        arguments:
        - params: The Parameters of the script.
        returns: The RequestHandler object linked to the type of database.
        throws: XalanihException if the kind of db is not supported.
        """
        assert isinstance(params,Parameters)
        database_type = params.get_database_type()
        if(database_type == Constants.DB_MYSQL):
            return MysqlRequestHandler()
        elif (database_type == Constants.DB_POSTGRESQL):
            return PostgreSQLRequestHandler()
        raise XalanihException("This type of database is not managed :" 
                                    + database_type + ".",
                                    XalanihException.DB_TYPE_NOT_SUPPORTED)
