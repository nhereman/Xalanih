# -*- coding: utf-8 -*-
import xalanih.core.parameters as parameters
from xalanih.core.dbcreator import DBCreator
from xalanih.core.dbupdator import DBUpdator
from xalanih.core.dbchecker import DBChecker
from xalanih.core.dbconnectorfactory import DBConnectorFactory
from xalanih.core.requesthandlerfactory import RequestHandlerFactory
from xalanih.core.xalanihexception import XalanihException
from xalanih.core.logger import Logger
from xalanih.core.constants import Constants
import sys
import traceback

# Get parameters
params = parameters.Parameters()
action = params.get_action()

# Get Logger
logger = Logger(params.get_log_file(), params.get_verbosity())

# noinspection PyBroadException
try:
    connection = DBConnectorFactory.get_connection(params, logger)
    request_handler = RequestHandlerFactory.get_request_handler(params)

    checker = DBChecker(connection, request_handler, logger)

    # Check if table already exists
    if action == Constants.ACTION_CHECK_DB:
        db_exists = checker.check_db_exists()
        sys.exit(0 if db_exists else XalanihException.TABLE_NOT_FOUND)

    # Creating database if required
    if action == Constants.ACTION_CREATE:
        creator = DBCreator(params.get_directory(), connection, request_handler,
                            logger)
        creator.create_database(checker)
        logger.debug("Committing transaction.")
        connection.commit()

    # Updating database if required
    no_update = params.get_no_update()
    if no_update and action == Constants.ACTION_CREATE:
        logger.info("The flag 'no update' is set. Skipping the updates.")
        
    if (action == Constants.ACTION_UPDATE or 
            (action == Constants.ACTION_CREATE and not no_update)):
        updater = DBUpdator(params.get_directory(), connection, request_handler,
                            logger)
        updater.apply_updates(checker, params.get_last_update())
        connection.commit()
        logger.debug("Committing transaction.")

    # Check last update
    if action == Constants.ACTION_CHECK_UPDATE:
        checker = DBChecker(connection, request_handler, logger)
        last_update = checker.check_last_update()
        print(last_update)

    logger.info("Done.")

except XalanihException as e:
    logger.error(e.args[0])
    logger.error("Stopping the execution of Xalanih.")
    if 'connection' in vars():
        logger.debug("Rollbacking transaction.")
        # noinspection PyUnboundLocalVariable
        connection.rollback()
    sys.exit(e.get_error_code())
except Exception as e:
    logger.error("Unexpected exception:\n {0}".format(traceback.format_exc()))
    logger.error("Stopping the execution of Xalanih.")
    if 'connection' in vars():
        logger.debug("Rollbacking transaction.")
        # noinspection PyUnboundLocalVariable
        connection.rollback()
    sys.exit(XalanihException.UNEXPECTED_EXCEPTION)
finally:
    if 'connection' in vars():
        logger.debug("Closing connection to database.")
        connection.close()
    logger.shutdown()
