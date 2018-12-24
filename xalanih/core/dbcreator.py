from xalanih.core.requesthandler import RequestHandler
from xalanih.core.sqlfileexecutor import SqlFileExecutor
from xalanih.core.xalanihexception import XalanihException
from xalanih.core.logger import Logger
from xalanih.core.constants import Constants
from xalanih.utils.parameters import Parameters
import sqlparse

class DBCreator:

    def __init__(self, directory, connection, request_handler, logger):
        """
        Constructor.
        arguments:
        - directory: The working directory.
        - connection: The connection object to the database.
        - request_handler: The RequestHandler associated to the type of db.
        - logger: The logger.
        """
        assert isinstance(request_handler, RequestHandler)
        assert isinstance(logger, Logger)
        self.directory = directory
        self.connection = connection
        self.request_handler = request_handler
        self.logger = logger

    def create_database(self, db_checker):
        """
        Execute the creation to the database.
        """
        if db_checker.check_db_exists():
            raise XalanihException("The table {0} already exists."
                                    .format(Constants.XALANIH_TABLE),
                                XalanihException.TABLE_EXISTS)
        self.logger.info("Creation of the database.")
        self.__create_xalanih_table()
        self.__execute_creation_script()
        self.__fill_xalanih_table()
        self.logger.info("Database created.")

    def __create_xalanih_table(self):
        """
        Create the xalanih table.
        throws: XalanihException if the table already exists.
        """
        self.logger.info("Creation of the table {0}."
                            .format(Constants.XALANIH_TABLE))
        sql_request = self.request_handler.request_xalanih_table_creation()
        self.logger.debug("[REQUEST]{0}".format(sql_request))
        self.connection.cursor().execute(sql_request)

    def __execute_creation_script(self):
        """
        Execute the script creation.sql.
        throws: XalanihException if the file can't be oppened.
        """
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

    def __fill_xalanih_table(self):
        """
        Fill the xalanih table with the list of update included 
        in the creation.
        """
        self.logger.info("Filling Xalanih table with updates included"
                            " in creation.")
        cursor = self.connection.cursor()

        try:
            filename = self.directory + "/" +Constants.PATH_INC_UPDATES
            self.logger.debug("Openning file with included updates: {0}"
                            .format(filename))
            # Initial creation
            sql_request = self.request_handler.request_update_recording()
            self.logger.debug("[REQUEST] {0}".format(sql_request))
            self.logger.debug("[REQUEST PARAMETERS] {0}"
                                .format([Constants.INITIAL_CREATION]))
            cursor.execute(sql_request, [Constants.INITIAL_CREATION])
            # Updates                
            inc_updates_file = open(filename)
            for line in inc_updates_file:
                if line != "":
                    update = line.strip()
                    self.logger.info("Registering update: {0}".format(update))
                    sql_request = self.request_handler.request_update_recording()
                    self.logger.debug("[REQUEST] {0}".format(sql_request))
                    self.logger.debug("[REQUEST PARAMETERS] {0}".format([update]))
                    cursor.execute(sql_request,[update])
            cursor.close()
            inc_updates_file.close()
        except IOError:
            self.logger.warning("Impossible to open the file containing" 
                                    " the included updates.")
            self.logger.warning("Skipping the filling of xalanih table.")

