import MySQLdb as db
from utils.parameters import Parameters
from core.dbconnector import DBConnector
from core.logger import Logger
from core.xalanihexception import XalanihException

class MysqlConnector(DBConnector):

    def __init__(self, params, logger):
        assert isinstance(params, Parameters)
        assert isinstance(logger, Logger)
        self.connectionInfo = params.getConnectionInfo()
        self.socket = params.getSocket()
        self.logger = logger
        self.connection = None

    def connect(self):
        if self.connection != None:
            raise XalanihException("You are already connected",
                                         XalanihException.ALREADY_CONNECTED)
        self.connection = db.connect(**self.__getConnectArgument())
        self.logger.info("Connected.")
        return self.connection

    def getConnection(self):
        return self.connection
        

    def __getConnectArgument(self):
        arguments = dict()
        host = self.connectionInfo.getHost()
        port = self.connectionInfo.getPort()
        database = self.connectionInfo.getDatabase()
        user = self.connectionInfo.getUser()
        password = self.connectionInfo.getPassword()

        arguments["host"] = host
        arguments["db"] = database
        arguments["user"] = user

        if port != None:
            arguments["port"] = port
        
        if password != None:
            arguments["passwd"] = password

        if self.socket!= None:
            arguments["unix_socket"] = self.socket

        return arguments
        
        



        


