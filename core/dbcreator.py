from core.requesthandler import RequestHandler
from core.sqlfileexecutor import SqlFileExecutor
from core.xalanihexception import XalanihException
from utils.parameters import Parameters
import sqlparse

class DBCreator:

    def __init__(self, directory, connection, request_handler):
        assert isinstance(request_handler, RequestHandler)
        self.directory = directory
        self.connection = connection
        self.request_handler = request_handler

    def createDatabase(self):
        self.__createXalanihTable()
        self.__executeCreationScript()
        self.__fillXalanihTable()

    def __createXalanihTable(self):
        if self.__doesXalanihTableExists():
            raise XalanihException("The table xalanih_updates already exists.",
                                XalanihException.TABLE_EXISTS)
        print("Creation of the table xalanih_updates ...")
        sqlRequest = self.request_handler.requestXalanihTableCreation()
        self.connection.query(sqlRequest)

    def __executeCreationScript(self):
        try:
            creation_file = open(self.directory +  "/creation/creation.sql")
            print("\tExecution of the creation script...")
            SqlFileExecutor.execute(self.connection, creation_file)                
        except IOError:
            raise XalanihException("The file 'creation/creation.sql'"
                                "can not be opened.",
                                XalanihException.NO_CREATION_SCRIPT)

    def __fillXalanihTable(self):
        cursor = self.connection.cursor()
        try:
            inc_updates_file = open(self.directory + "creation/included_updates")
            for line in inc_updates_file:
                if line != "":
                    update = line.strip()
                    print("\tApplying the update " + update + ".")
                    sqlRequest = self.request_handler.requestUpdateRecording()
                    cursor.execute(sqlRequest,[update])
            cursor.close()
        except IOError:
            print("The file creation/included_updates does not exist."
                    "Skipping the filling step.")

    def __doesXalanihTableExists(self):
        request = self.request_handler.requestXalanihTable()
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