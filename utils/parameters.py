##-*- coding: utf-8 -*-
import argparse
from core.connectioninfo import *

class Parameters:

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Xalanih: Database versioning helper.")
        # Action param
        self.parser.add_argument("action",
                choices=["create", "update"],
                help="Give the action to execute. create: Create \
                the database from zero. update: execute the needed \
                update scripts on an existing database")

        # DB files directory
        self.parser.add_argument("-d","--directory",
                dest= "directory",
                default=".")

        # DB Type
        self.parser.add_argument("-t", "--type",
                choices=["mysql", "postgresql"],
                dest="type",
                default="mysql",
                help="Select the type of database. (i.e. mysql)")

        # Host
        self.parser.add_argument("-H", "--host",
                dest="host",
                default="localhost",
                help="The hostname of the database")

        # Port
        self.parser.add_argument("-p", "--port",
                dest="port",
                help="The port of the database")

        # DB
        self.parser.add_argument("database",
                help="The database")

        # User
        self.parser.add_argument("-u", "--user",
                dest="user",
                default="root")
        
        # Password
        self.parser.add_argument("-pwd", "-password",
                dest="password")

        # Socket
        self.parser.add_argument("-s", "--socket",
                dest="socket")
                
        self.args = self.parser.parse_args()

        # Define connection info
        self.__defineConnectionInfo()

    def __defineConnectionInfo(self):
            assert self.args.port.isnumeric()
            self.connectionInfo = ConnectionInfo(host=self.args.host,
                        port=int(self.args.port), database=self.args.database,
                        user=self.args.user, password=self.args.password)

    def getArguments(self):
        return self.args

    def getAction(self):
        return self.args.action

    def getDirectory(self):
        return self.args.directory

    def getTypeOfDatabase(self):
        return self.args.type

    def getConnectionInfo(self):
            return self.connectionInfo

    def getSocket(self):
        return self.args.socket
        