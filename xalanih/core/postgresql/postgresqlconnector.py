import psycopg2 as db
from xalanih.core.parameters import Parameters
from xalanih.core.dbconnector import DBConnector
from xalanih.core.logger import Logger
from xalanih.core.xalanihexception import XalanihException


class PostgreSQLConnector(DBConnector):

    def __init__(self, params, logger):
        """
        Constructor.
        arguments:
        - params: The parameters of the script.
        - logger: The logger.
        """
        assert isinstance(params, Parameters)
        assert isinstance(logger, Logger)
        self.connectionInfo = params.get_connection_info()
        self.socket = params.get_socket()
        self.logger = logger
        self.connection = None

    def connect(self):
        """
        Establish a connection with the database.
        returns: The connection object.
        """
        if self.connection is not None:
            raise XalanihException("You are already connected",
                                   XalanihException.ALREADY_CONNECTED)
        self.connection = db.connect(**self.__get_connect_argument())
        self.logger.info("Connected.")
        return self.connection

    def get_connection(self):
        """
        returns: The connection object if connected. None otherwise.
        """
        return self.connection

    def __get_connect_argument(self):
        """
        Return the list of arguments used to connect to the mysql database.
        returns: The list of arguments used to connect to the mysql database.
        """
        arguments = dict()
        host = self.connectionInfo.get_host()
        port = self.connectionInfo.get_port()
        database = self.connectionInfo.get_database()
        user = self.connectionInfo.get_user()
        password = self.connectionInfo.get_password()

        arguments["host"] = host
        arguments["dbname"] = database
        arguments["user"] = user

        if port is not None:
            arguments["port"] = port

        if password is not None:
            arguments["password"] = password

        return arguments
