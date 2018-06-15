from utils.parameters import Parameters
from core.mysql.mysqlconnector import MysqlConnector

class DBConnector:
    @staticmethod
    def getConnector(params):
        assert isinstance(params,Parameters)
        return MysqlConnector(params)
        