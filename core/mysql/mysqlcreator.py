from core.dbcreator import DBCreator
from core.mysql.mysqlconnector import MysqlConnector
from core.mysql.mysqlchecker import MysqlChecker
from core.mysql.mysqlfileexecutor import MysqlFileExecutor
from utils.parameters import Parameters
import sqlparse

class MysqlCreator(DBCreator):

    def __init__(self, params, connector, checker):
        assert isinstance(params, Parameters)
        assert isinstance(connector, MysqlConnector)
        assert isinstance(checker, MysqlChecker)
        self.params = params
        self.connector = connector
        self.checker = checker

    def createDatabase(self):
        self.__createXalanihTable()
        self.__executeCreationScript()
        self.__fillXalanihTable()

    def __createXalanihTable(self):
        if self.checker.doesXalanihTableExists():
            raise Exception("MysqlCreator-__createXalanihTable: The table "
                                "xalanih_updates already exists. Stopping the "
                                "creation of the database.")
        print("Creation of the table xalanih_updates ...")
        self.connector.getConnection().query(
            "CREATE TABLE xalanih_updates (\
                `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,\
                `update_name` VARCHAR(150) NOT NULL,\
                `update_apply_time` TIME NOT NULL,\
                PRIMARY KEY (`id`));"
        )
    
    def __executeCreationScript(self):
        try:
            creation_file = open(self.params.getDirectory() +  "/creation/creation.sql")
            print("\tExecution of the creation script...")
            MysqlFileExecutor.execute(self.connector, creation_file)                
        except IOError:
            raise Exception("The file 'creation/creation.sql' can not be opened.")

    def __fillXalanihTable(self):
        cursor = self.connector.getConnection().cursor()
        try:
            inc_updates_file = open(self.params.getDirectory() + "creation/included_updates")
            for line in inc_updates_file:
                if line != "":
                    update = line.strip()
                    print("\tApplying the update " + update + ".")
                    cursor.execute(
                        "INSERT INTO xalanih_updates (`update_name`, `update_apply_time`)"
                        "VALUES (%s, NOW())",[update])
            self.connector.getConnection().commit()
        except IOError:
            print("The file creation/included_updates does not exist. Skipping the filling step.")