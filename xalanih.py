##-*- coding: utf-8 -*-
from utils import parameters
from core.dbcreatorfactory import DBCreatorFactory
from core import dbupdator
from core.dbconnectorfactory import DBConnectorFactory
from core.dbcheckerfactory import DBCheckerFactory

params = parameters.Parameters()
action = params.getAction()

print("Directory: " + params.getDirectory())
print("Database type: " + params.getTypeOfDatabase())

connector = DBConnectorFactory.getConnector(params)
print("Connection to the database ...")
connector.connect()
print("Connected.")

checker = DBCheckerFactory.getChecker(params, connector)

if (action == "create"):
    print("Creating db ...")
    creator = DBCreatorFactory.getCreator(params,connector, checker)
    updator = dbupdator.DBUpdator(params)
    
    creator.createDatabase()
elif (action == "update"):
    print("Updating db ...")
    updator = dbupdator.DBUpdator(params)