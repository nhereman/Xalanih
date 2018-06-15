##-*- coding: utf-8 -*-
from utils import parameters
from core import dbcreator
from core import dbupdator

params = parameters.Parameters()
action = params.getAction()

print("Directory = " + params.getDirectory())

if (action == "create"):
    print("Creating db ...")
    creator = dbcreator.DBCreator(params)
elif (action == "update"):
    print("Updating db ...")
    updator = dbupdator.DBUpdator(params)