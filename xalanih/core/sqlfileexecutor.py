from xalanih.core.logger import Logger
import sqlparse


class SqlFileExecutor:
    @staticmethod
    def execute(connection, sql_file, logger):
        """
        Execute the sql queries from a file.
        arguments:
        - sql_file: The sql file to execute.
        - logger: The logger.
        """
        assert isinstance(logger, Logger)
        logger.debug("Executing SQL file: {0}".format(sql_file.name))
        sql_statements = sqlparse.split(sql_file.read())
        cursor = connection.cursor()
        for sql in sql_statements:
            if sql != "":
                logger.debug("[REQUEST] {0}".format(sql))
                cursor.execute(sql)
        cursor.close()
