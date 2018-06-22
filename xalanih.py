##-*- coding: utf-8 -*-
from utils import parameters
from core.dbcreator import DBCreator
from core.dbupdator import DBUpdator
from core.dbconnectorfactory import DBConnectorFactory
from core.requesthandlerfactory import RequestHandlerFactory

# Get parameters
params = parameters.Parameters()
action = params.getAction()

print("Directory: " + params.getDirectory())
print("Database type: " + params.getTypeOfDatabase())

# Connecting database
print("Connection to the database ...")
connection = DBConnectorFactory.getConnection(params)
request_handler = RequestHandlerFactory.getRequestHandler(params)
print("Connected.")

if (action == "create"):
    print("Creating db ...")
    creator = DBCreator(params.getDirectory(), connection, request_handler)
    updator = DBUpdator(params.getDirectory(),connection,request_handler)
    creator.createDatabase()
    updator.applyUpdates()
elif (action == "update"):
    print("Updating db ...")
    updator = DBUpdator(params.getDirectory(),connection,request_handler)
    updator.applyUpdates()