import sqlparse

class SqlFileExecutor:
    @staticmethod
    def execute(connection, sqlFile):
        sql_statements = sqlparse.split(sqlFile.read())
        cursor = connection.cursor()
        for sql in sql_statements:
            if sql != "":
                cursor.execute(sql)
