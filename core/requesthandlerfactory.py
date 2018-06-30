from utils.parameters import Parameters
from core.mysql.mysqlrequesthandler import MysqlRequestHandler
from core.xalanihexception import XalanihException
from core.constants import Constants


class RequestHandlerFactory:
    @staticmethod
    def getRequestHandler(params):
        assert isinstance(params,Parameters)
        dbType = params.getTypeOfDatabase()
        if(dbType == Constants.DB_MYSQL):
            return MysqlRequestHandler()
        raise XalanihException("This type of database is not managed :" 
                                    + dbType + ".",
                                    XalanihException.DB_TYPE_NOT_SUPPORTED)