from utils.parameters import Parameters
from core.mysql.mysqlrequesthandler import MysqlRequestHandler
from core.xalanihexception import XalanihException

class RequestHandlerFactory:
    @staticmethod
    def getRequestHandler(params):
        assert isinstance(params,Parameters)
        dbType = params.getTypeOfDatabase()
        if(dbType == "mysql"):
            return MysqlRequestHandler()
        raise XalanihException("This type of database is not managed :" 
                                    + dbType + ".",
                                    XalanihException.DB_TYPE_NOT_SUPPORTED)