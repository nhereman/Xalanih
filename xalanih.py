##-*- coding: utf-8 -*-
from utils import parameters
from core import dbcreator
from core import dbupdator
from core.dbconnector import DBConnector

params = parameters.Parameters()
action = params.getAction()

print("Directory: " + params.getDirectory())
print("Database type: " + params.getTypeOfDatabase())

connector = DBConnector.getConnector(params)
print("Connection to the database ...")
connection = connector.connect()
print("Connected.")

if (action == "create"):
    print("Creating db ...")
    creator = dbcreator.DBCreator(params)
elif (action == "update"):
    print("Updating db ...")
    updator = dbupdator.DBUpdator(params)