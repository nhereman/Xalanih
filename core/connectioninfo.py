##-*- coding: utf-8 -*-

class ConnectionInfo:
    """
    Contains all the informations to connect to the database.
    """

    def __init__(self,host=None,port=None,database=None,user=None,
                    password=None):
        if host != None:
            self.setHost(host)
        if port != None:
            self.setPort(port)
        if database != None:
            self.setDatabase(database)
        if user != None:
            self.setUser(user)
        if password != None:
            self.setPassword(password)

    def setHost(self,host):
        assert (isinstance(host,str))
        self.host = host
    
    def setPort(self,port):
        assert isinstance(port,int)
        self.port = port

    def setDatabase(self,database):
        assert isinstance(database,str)
        self.database = database

    def setUser(self, user):
        assert isinstance(user,str)
        self.user = user

    def setPassword(self, password):
        assert isinstance(password, str)
        self.password = password

    def getHost(self):
        return self.host
    
    def getPort(self):
        return self.port

    def getDatabase(self):
        return self.database

    def getUser(self):
        return self.user

    def getPassword(self):
        return self.password