from core.mysql.mysqlconnector import MysqlConnector
from core.sqlfileexecutor import SqlFileExecutor
from core.requesthandler import RequestHandler
from utils.parameters import Parameters
from core.logger import Logger
from core.xalanihexception import XalanihException
import sqlparse
import os

class DBUpdator:

    def __init__(self, directory, connection, request_handler, logger):
        assert isinstance(request_handler,RequestHandler)
        assert isinstance(logger, Logger)
        self.directory = directory
        self.connection = connection
        self.request_handler = request_handler
        self.logger = logger

    def applyUpdates(self, last_update):
        self.logger.info("Updating database.")
        if not self.__doesXalanihTableExists():
            raise XalanihException("The xalanih table does not exist.",
                                    XalanihException.TABLE_NOT_FOUND)
        updatesToApply = self.__getListOfUpdatesToApply(last_update)
        self.logger.info("Application of {0} updates."
                            .format(len(updatesToApply)))
        for update in updatesToApply:
            self.__applyUpdate(update)
        self.logger.info("Database updated.")

    def __getListOfUpdatesToApply(self, last_update):
        updates = self.__getListOfUpdates()
        updates = self.__removeUpdatesAfter(updates, last_update)
        return self.__removeUpdatesAlreadyApplied(updates)

    def __applyUpdate(self, update):
        self.logger.info("Applying update " + update + ".")
        filepath = self.directory + "/update/" + update + ".sql"
        updateFile = open(filepath)
        SqlFileExecutor.execute(self.connection, updateFile, self.logger)
        self.__recordUpdate(update)

    def __getListOfUpdates(self):
        directory = self.directory + "/update"
        self.logger.debug("Getting list of sql files in directory: {0}"
                            .format(directory))
        files = os.listdir(directory)
        return [f[:-4] for f in files if f.endswith(".sql")]

    def __removeUpdatesAfter(self, updates, last_update):
        if last_update == None:
            return updates
        self.logger.debug("Filtering updates after {0}".format(last_update))
        try:
            index = updates.index(last_update)
            return updates[:index+1]
        except ValueError:
            raise XalanihException("The update {0} does not exist."
                                        .format(last_update),
                                    XalanihException.UPDATE_NOT_FOUD)

    def __removeUpdatesAlreadyApplied(self, updates):
        return [update for update in updates 
                    if not self.__isUpdateAlreadyApplied(update)]

    def __recordUpdate(self, update):
        self.logger.debug("Registering update: {0}".format(update))
        cursor = self.connection.cursor()
        request = self.request_handler.requestUpdateRecording()
        self.logger.debug("[REQUEST] {0}".format(request))
        self.logger.debug("[REQUEST PARAMETERS] {0}".format([update]))
        cursor.execute(request ,[update])
        cursor.close()

    def __isUpdateAlreadyApplied(self, update):
        self.logger.debug("Looking if the update {0} has already been applied."
                            .format(update))
        cursor = self.connection.cursor()
        request = self.request_handler.requestUpdate()
        self.logger.debug("[REQUEST] {0}".format(request))
        self.logger.debug("[REQUEST PARAMETERS] {0}".format([update]))
        cursor.execute(request,[update])
        self.logger.debug("[REQUEST RESULT] Number of entries found: {0}"
                            .format(cursor.rowcount))
        cursor.close()
        return cursor.rowcount == 1

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
            if result[0] == "xalanih_updates":
                return True
        return False