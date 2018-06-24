from core.mysql.mysqlconnector import MysqlConnector
from core.sqlfileexecutor import SqlFileExecutor
from utils.parameters import Parameters
import sqlparse
import os

class DBUpdator:

    def __init__(self, directory, connection, request_handler):
        self.directory = directory
        self.connection = connection
        self.request_handler = request_handler

    def applyUpdates(self):
        print("Updating database ...")
        updatesToApply = self.__getListOfUpdatesToApply()
        for update in updatesToApply:
            self.__applyUpdate(update)

    def __getListOfUpdatesToApply(self):
        fullUpdateList = self.__getListOfUpdates()
        return self.__removeUpdatesAlreadyApplied(fullUpdateList)

    def __applyUpdate(self, update):
        print("\tApplying update " + update + ".")
        filepath = self.directory + "/update/" + update + ".sql"
        updateFile = open(filepath)
        SqlFileExecutor.execute(self.connection, updateFile)
        self.__recordUpdate(update)

    def __getListOfUpdates(self):
        files = os.listdir(self.directory + "/update")
        return [f[:-4] for f in files if f.endswith(".sql")]

    def __removeUpdatesAlreadyApplied(self, updates):
        return [update for update in updates 
                    if not self.__isUpdateAlreadyApplied(update)]

    def __recordUpdate(self, update):
        cursor = self.connection.cursor()
        cursor.execute(self.request_handler.requestUpdateRecording(),[update])
        cursor.close()

    def __isUpdateAlreadyApplied(self, update):
        cursor = self.connection.cursor()
        cursor.execute(self.request_handler.requestUpdate(),[update])
        cursor.close()
        return cursor.rowcount == 1