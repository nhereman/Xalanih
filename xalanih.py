##-*- coding: utf-8 -*-
from utils import parameters
from core.dbcreator import DBCreator
from core.dbupdator import DBUpdator
from core.dbconnectorfactory import DBConnectorFactory
from core.requesthandlerfactory import RequestHandlerFactory
from core.xalanihexception import XalanihException
from core.logger import Logger
import sys
import traceback

# Get parameters
params = parameters.Parameters()
action = params.getAction()

# Get Logger
logger = Logger(params.getLogfile(), params.getVerbosity())

# Connecting database

try:
    connection = DBConnectorFactory.getConnection(params, logger)
    request_handler = RequestHandlerFactory.getRequestHandler(params)

    if (action == "create"):
        creator = DBCreator(params.getDirectory(), connection, request_handler,
                                logger)
        creator.createDatabase()
        logger.debug("Committing transaction.")
        connection.commit()
    if (action == "update" or action == "create"):
        updator = DBUpdator(params.getDirectory(),connection,request_handler,
                                logger)
        updator.applyUpdates()
        connection.commit()
        logger.debug("Committing transaction.")

    logger.info("Done.")

except XalanihException as e:
    logger.error(e.args[0])
    logger.error("Stopping the execution of Xalanih.")
    if 'connection' in vars():
        logger.debug("Rollbacking transaction.")
        connection.rollback()
    sys.exit(e.getErrorCode())
except Exception as e:
    logger.error("Unexpected exception:\n {0}".format(traceback.format_exc()))
    logger.error("Stopping the execution of Xalanih.")
    if 'connection' in vars():
        logger.debug("Rollbacking transaction.")
        connection.rollback()
    sys.exit(XalanihException.UNEXPECTED_EXCEPTION)
finally:
    if 'connection' in vars():
        logger.debug("Closing connection to database.")
        connection.close()
    logger.shutdown()
    