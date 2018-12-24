from xalanih.core.requesthandler import RequestHandler
from xalanih.core.logger import Logger
from xalanih.core.constants import Constants
from xalanih.core.xalanihexception import XalanihException


class DBChecker:

    def __init__(self, connection, request_handler, logger):
        """
        Constructor.
        arguments:
            - connection: The connection object to the database.
            - request_handler: The RequestHandler associated to the type of db.
            - logger: The logger.
        """
        assert isinstance(request_handler, RequestHandler)
        assert isinstance(logger, Logger)

        self.connection = connection
        self.request_handler = request_handler
        self.logger = logger

    def check_last_update(self):
        """
        Get the last update
        """
        self.logger.info("Checking last update.")

        if not self.check_db_exists():
            raise XalanihException("The table {0} does not exist."
                                   .format(Constants.XALANIH_TABLE),
                                   XalanihException.TABLE_NOT_FOUND)

        cursor = self.connection.cursor()
        request = self.request_handler.request_last_update()
        self.logger.debug("[REQUEST] {0}".format(request))

        cursor.execute(request)
        result = cursor.fetchone()
        cursor.close()

        self.logger.debug("[REQUEST RESULT] {0}".format(result[0]))
        return result[0]

    def check_db_exists(self):
        """
        Check if the xalanih table exists in the database.
        """
        self.logger.debug("Checking if the xalanih table already exists.")
        request = self.request_handler.request_xalanih_table()
        self.logger.debug("[REQUEST] {0}".format(request))
        cursor = self.connection.cursor()
        cursor.execute(request)
        results = cursor.fetchall()
        cursor.close()
        return self.__contains_xalanih_table(results)

    @staticmethod
    def __contains_xalanih_table(results):
        """
        Check if the given parameter contains the xalanih table.
        arguments:
        - results: The result to the sql request looking for xalanih table.
                    format: [(table1,), (table2,), ...]
        returns: True if present, False otherwise.
        """
        for result in results:
            if result[0] == Constants.XALANIH_TABLE:
                return True
        return False
