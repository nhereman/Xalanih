from xalanih.core.mysql.mysqlconnector import MysqlConnector
from xalanih.core.sqlfileexecutor import SqlFileExecutor
from xalanih.core.requesthandler import RequestHandler
from xalanih.utils.parameters import Parameters
from xalanih.core.logger import Logger
from xalanih.core.xalanihexception import XalanihException
from xalanih.core.constants import Constants
import sqlparse
import os

class DBUpdator:

    def __init__(self, directory, connection, request_handler, logger):
        """
        Constructor.
        arguments:
        - directory: The working directory.
        - connection: The connection object to the database.
        - request_handler: The request handler associated to the type of db.
        - logger: The logger.
        """
        assert isinstance(request_handler,RequestHandler)
        assert isinstance(logger, Logger)
        self.directory = directory
        self.connection = connection
        self.request_handler = request_handler
        self.logger = logger

    def apply_updates(self, last_update):
        """
        Apply the updates to the database.
        arguments:
        - last_update: the name of the last update that must be applied.
        throws:
        - XalanihException if the xalanih table is not present in db.
        - XalanihException if the last_update does not exists.
        """
        self.logger.info("Updating database.")
        if not self.__does_xalanih_table_exists():
            raise XalanihException("The xalanih table does not exist.",
                                    XalanihException.TABLE_NOT_FOUND)
        updates_to_apply = self.__get_list_of_updates_to_apply(last_update)
        self.logger.info("Application of {0} updates."
                            .format(len(updates_to_apply)))
        for update in updates_to_apply:
            self.__apply_update(update)
        self.logger.info("Database updated.")

    def __get_list_of_updates_to_apply(self, last_update):
        """
        Get the list of updates that must be applied.
        arguments:
        - last_update: the name of the last update that must be applied.
        returns: The list of updates that must be applied.
        """
        updates = self.__get_list_of_updates()
        updates = self.__remove_updates_after(updates, last_update)
        return self.__remove_updates_already_applied(updates)

    def __apply_update(self, update):
        """
        Apply the update given in parameter.
        arguments:
        - updates: The name of the update that will be applied.
        """
        self.logger.info("Applying update " + update + ".")
        filepath = (self.directory + "/" + Constants.DIR_UPDATE + "/" + update 
                        + ".sql")
        updateFile = open(filepath)
        SqlFileExecutor.execute(self.connection, updateFile, self.logger)
        updateFile.close()
        self.__record_update(update)

    def __get_list_of_updates(self):
        """
        Give the list of updates present in the update directory.
        returns: The list of updates present in the update directory.
        """
        directory = self.directory + "/" + Constants.DIR_UPDATE
        self.logger.debug("Getting list of sql files in directory: {0}"
                            .format(directory))
        files = os.listdir(directory)
        result = [f[:-4] for f in files if f.endswith(".sql")]
        result.sort()
        return result

    def __remove_updates_after(self, updates, last_update):
        """
        Remove the updates after the last update in the list.
        arguments:
        - updates: The list of updates to filter.
        - last_update: The last update of the filtered list.
        returns: The list filtered with all the updates after 
                last_update removed.
        throws: XalanihException if the last_update does not exists.
        """
        if last_update == None:
            return updates
        self.logger.debug("Filtering updates after {0}".format(last_update))
        try:
            index = updates.index(last_update)
            return updates[:index+1]
        except ValueError:
            raise XalanihException("The update {0} does not exist."
                                        .format(last_update),
                                    XalanihException.UPDATE_NOT_FOUND)

    def __remove_updates_already_applied(self, updates):
        """
        Remove all the updates already applied from the list.
        arguments:
        - updates: The list of updates to filter.
        returns: The list of update without the one already applied.
        """
        return [update for update in updates 
                    if not self.__is_update_already_applied(update)]

    def __record_update(self, update):
        self.logger.debug("Registering update: {0}".format(update))
        cursor = self.connection.cursor()
        request = self.request_handler.request_update_recording()
        self.logger.debug("[REQUEST] {0}".format(request))
        self.logger.debug("[REQUEST PARAMETERS] {0}".format([update]))
        cursor.execute(request ,[update])
        cursor.close()

    def __is_update_already_applied(self, update):
        """
        Check if an update has already been applied.
        arguments:
        - update: The update to check.
        return: True if the update has already been applied. False otherwise.
        """
        self.logger.debug("Looking if the update {0} has already been applied."
                            .format(update))
        cursor = self.connection.cursor()
        request = self.request_handler.request_update()
        self.logger.debug("[REQUEST] {0}".format(request))
        self.logger.debug("[REQUEST PARAMETERS] {0}".format([update]))
        cursor.execute(request,[update])
        self.logger.debug("[REQUEST RESULT] Number of entries found: {0}"
                            .format(cursor.rowcount))
        cursor.close()
        return cursor.rowcount == 1

    def __does_xalanih_table_exists(self):
        """
        Check if the Xalanih table already exists.
        return: True if the table already exists. False otherwise.
        """
        self.logger.debug("Checking if the xalanih table already exists.")
        request = self.request_handler.request_xalanih_table()
        self.logger.debug("[REQUEST] {0}".format(request))
        cursor = self.connection.cursor()
        cursor.execute(request)
        results = cursor.fetchall()
        cursor.close()
        return self.__contains_xalanih_table(results)

    def __contains_xalanih_table(self, results):
        """
        Check if the given parameter contains the xalanih table.
        arguments:
        - results: The result to the sql request looking for xalanih table.
        returns: True if present, False otherwise.
        """
        for result in results:
            if result[0] == Constants.XALANIH_TABLE:
                return True
        return False
