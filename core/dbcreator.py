from core.requesthandler import RequestHandler
from core.sqlfileexecutor import SqlFileExecutor
from core.xalanihexception import XalanihException
from core.logger import Logger
from core.constants import Constants
from utils.parameters import Parameters
import sqlparse

class DBCreator:

    def __init__(self, directory, connection, request_handler, logger):
        assert isinstance(request_handler, RequestHandler)
        assert isinstance(logger, Logger)
        self.directory = directory
        self.connection = connection
        self.request_handler = request_handler
        self.logger = logger

    def createDatabase(self):
        self.logger.info("Creation of the database.")
        self.__createXalanihTable()
        self.__executeCreationScript()
        self.__fillXalanihTable()
        self.logger.info("Database created.")

    def __createXalanihTable(self):
        if self.__doesXalanihTableExists():
            raise XalanihException("The table {0} already exists."
                                    .format(Constants.XALANIH_TABLE),
                                XalanihException.TABLE_EXISTS)
        self.logger.info("Creation of the table {0}."
                            .format(Constants.XALANIH_TABLE))
        sqlRequest = self.request_handler.requestXalanihTableCreation()
        self.logger.debug("[REQUEST]{0}".format(sqlRequest))
        self.connection.query(sqlRequest)

    def __executeCreationScript(self):
        try:
            filename = self.directory +  Constants.PATH_CREATION
            self.logger.info("Execution of the creation script.")
            creation_file = open(filename)
            SqlFileExecutor.execute(self.connection, creation_file,
                                        self.logger)
            creation_file.close()                
        except IOError:
            raise XalanihException("The file '{0}' can not be opened."
                                    .format(filename),
                                    XalanihException.NO_CREATION_SCRIPT)

    def __fillXalanihTable(self):
        self.logger.info("Filling Xalanih table with updates included"
                            " in creation.")
        cursor = self.connection.cursor()
        try:
            filename = self.directory + Constants.PATH_INC_UPDATES
            self.logger.debug("Openning file with included updates: {0}"
                            .format(filename))
            inc_updates_file = open(filename)
            for line in inc_updates_file:
                if line != "":
                    update = line.strip()
                    self.logger.info("Registering update: {0}".format(update))
                    sqlRequest = self.request_handler.requestUpdateRecording()
                    self.logger.debug("[REQUEST] {0}".format(sqlRequest))
                    self.logger.debug("[REQUEST PARAMETERS] {0}".format([update]))
                    cursor.execute(sqlRequest,[update])
            cursor.close()
        except IOError:
            self.logger.warning("Impossible to open the file containing" 
                                    " the included updates.")
            self.logger.warning("Skipping the filling of xalanih table.")

    def __doesXalanihTableExists(self):
        self.logger.debug("Checking if the xalanih table already exists.")
        request = self.request_handler.requestXalanihTable()
        self.logger.debug("[REQUEST] {0}".format(request))
        cursor = self.connection.cursor()
        cursor.execute(request)
        results = cursor.fetchall()
        cursor.close()
        return self.__doesResultsContainsXalanihTable(results)

    def __doesResultsContainsXalanihTable(self, results):
        for result in results:
            if result[0] == Constants.XALANIH_TABLE:
                return True
        return False