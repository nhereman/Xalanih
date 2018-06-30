from core.mysql.mysqlconnector import MysqlConnector
from core.sqlfileexecutor import SqlFileExecutor
from core.requesthandler import RequestHandler
from utils.parameters import Parameters
from core.logger import Logger
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

    def applyUpdates(self):
        self.logger.info("Updating database.")
        updatesToApply = self.__getListOfUpdatesToApply()
        self.logger.info("Application of {0} updates."
                            .format(len(updatesToApply)))
        for update in updatesToApply:
            self.__applyUpdate(update)
        self.logger.info("Database updated.")

    def __getListOfUpdatesToApply(self):
        fullUpdateList = self.__getListOfUpdates()
        return self.__removeUpdatesAlreadyApplied(fullUpdateList)

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