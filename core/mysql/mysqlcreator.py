from core.dbcreator import DBCreator
from core.mysql.mysqlconnector import MysqlConnector
from core.mysql.mysqlchecker import MysqlChecker
from utils.parameters import Parameters

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
            raise Exception("MysqlCreator-__createXalanihTable: The table \
                                xalanih_updates already exists. Stopping the \
                                creation of the database.")
        print("Creation of the table xalanih_updates ...")
        self.connector.getConnection().query(
            "CREATE TABLE xalanih_updates (\
                `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,\
                `update_name` VARCHAR(150) NOT NULL,\
                `update_apply_time` TIME NOT NULL,\
                PRIMARY KEY (`id`));"
        )
    
    def __executeCreationScript(self):
        pass # TODO

    def __fillXalanihTable(self):
        pass # TODO