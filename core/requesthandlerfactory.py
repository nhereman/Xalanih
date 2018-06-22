from utils.parameters import Parameters
from core.mysql.mysqlrequesthandler import MysqlRequestHandler

class RequestHandlerFactory:
    @staticmethod
    def getRequestHandler(params):
        assert isinstance(params,Parameters)
        dbType = params.getTypeOfDatabase()
        if(dbType == "mysql"):
            return MysqlRequestHandler()
        raise Exception("This type of database is not managed :" 
                            + dbType + ".")