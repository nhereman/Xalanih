from core.mysql.mysqlconnector import MysqlConnector
import MySQLdb as db
import sqlparse

class MysqlFileExecutor:
    @staticmethod
    def execute(connector, sqlFile):
        assert isinstance(connector, MysqlConnector)
        sql_statements = sqlparse.split(sqlFile.read())
        cursor = connector.getConnection().cursor()
        for sql in sql_statements:
            if sql != "":
                cursor.execute(sql)
