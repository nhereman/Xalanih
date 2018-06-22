from core.dbupdator import DBUpdator
from core.mysql.mysqlconnector import MysqlConnector
from core.mysql.mysqlchecker import MysqlChecker
from core.mysql.mysqlfileexecutor import MysqlFileExecutor
from utils.parameters import Parameters
import sqlparse
import os

class MysqlUpdator(DBUpdator):

    def __init__(self, params, connector, checker):
        assert isinstance(params, Parameters)
        assert isinstance(connector, MysqlConnector)
        assert isinstance(checker, MysqlChecker)

        self.params = params
        self.connector = connector
        self.checker = checker

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
        filepath = self.params.getDirectory() + "/update/" + update + ".sql"
        updateFile = open(filepath)
        MysqlFileExecutor.execute(self.connector, updateFile)
        self.__recordUpdate(update)

    def __getListOfUpdates(self):
        files = os.listdir(self.params.getDirectory() + "/update")
        return [f[:-4] for f in files if f.endswith(".sql")]

    def __removeUpdatesAlreadyApplied(self, updates):
        return [update for update in updates if not self.__isUpdateAlreadyApplied(update)]

    def __recordUpdate(self, update):
        cursor = self.connector.getConnection().cursor()
        cursor.execute(
                        "INSERT INTO xalanih_updates (`update_name`, `update_apply_time`)"
                        "VALUES (%s, NOW())",[update])
        self.connector.getConnection().commit()

    def __isUpdateAlreadyApplied(self, update):
        cursor = self.connector.getConnection().cursor()
        cursor.execute("SELECT * FROM xalanih_updates WHERE update_name = %s",
                            [update])
        return cursor.rowcount == 1