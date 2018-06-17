from core.dbchecker import DBChecker
from core.mysql.mysqlconnector import MysqlConnector
from utils.parameters import Parameters

class MysqlChecker(DBChecker):

    def __init__(self, params, connector):
        assert isinstance(params, Parameters)
        assert isinstance(connector, MysqlConnector)
        self.params = params
        self.connector = connector

    def doesXalanihTableExists(self):
        cursor = self.connector.getConnection().cursor()
        cursor.execute("SHOW TABLES")
        results = cursor.fetchall()
        return self.__doesResultsContainsXalanihTable(results)

    def __doesResultsContainsXalanihTable(self, results):
        for result in results:
            if result[0] == "xalanih_updates":
                return True
        return False