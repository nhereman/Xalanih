##-*- coding: utf-8 -*-
from utils import parameters
from core.dbcreatorfactory import DBCreatorFactory
from core.dbupdatorfactory import DBUpdatorFactory
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
    updator = DBUpdatorFactory.getUpdator(params,connector,checker)
    
    creator.createDatabase()
    updator.applyUpdates()
elif (action == "update"):
    print("Updating db ...")
    updator = DBUpdatorFactory.getUpdator(params,connector,checker)
    updator.applyUpdates()