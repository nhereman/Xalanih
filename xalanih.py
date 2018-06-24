##-*- coding: utf-8 -*-
from utils import parameters
from core.dbcreator import DBCreator
from core.dbupdator import DBUpdator
from core.dbconnectorfactory import DBConnectorFactory
from core.requesthandlerfactory import RequestHandlerFactory
from core.xalanihexception import XalanihException
import sys

# Get parameters
params = parameters.Parameters()
action = params.getAction()

print("Directory: " + params.getDirectory())
print("Database type: " + params.getTypeOfDatabase())

# Connecting database

try:
    print("Connection to the database ...")
    connection = DBConnectorFactory.getConnection(params)
    request_handler = RequestHandlerFactory.getRequestHandler(params)
    print("Connected.")
    if (action == "create"):
        print("Creating db ...")
        creator = DBCreator(params.getDirectory(), connection, request_handler)
        creator.createDatabase()
        connection.commit()
    if (action == "update" or action == "create"):
        print("Updating db ...")
        updator = DBUpdator(params.getDirectory(),connection,request_handler)
        updator.applyUpdates()
        connection.commit()
    connection.close()
except XalanihException as e:
    print("ERROR: {0}".format(e.args[0]))
    print("ERROR: Stopping the creation of the database.")
    connection.rollback()
    sys.exit(e.getErrorCode())
except Exception as e:
    print("ERROR: Unexpected exception")
    print("ERROR: Stopping the creation of the database.")
    connection.rollback()
    raise e