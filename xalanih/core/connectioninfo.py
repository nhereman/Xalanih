##-*- coding: utf-8 -*-

class ConnectionInfo:
    """
    Contains all the informations to connect to the database.
    """

    def __init__(self,host=None,port=None,database=None,user=None,
                    password=None):
        self.set_host(host)
        self.set_port(port)
        self.set_database(database)
        self.set_user(user)
        self.set_password(password)

    def set_host(self,host):
        assert ((isinstance(host,str)) or host == None)
        self.host = host
    
    def set_port(self,port):
        assert (isinstance(port,int) or port == None)
        self.port = port

    def set_database(self,database):
        assert (isinstance(database,str) or database == None)
        self.database = database

    def set_user(self, user):
        assert (isinstance(user,str) or user == None)
        self.user = user

    def set_password(self, password):
        assert (isinstance(password, str) or password == None)
        self.password = password

    def get_host(self):
        return self.host
    
    def get_port(self):
        return self.port

    def get_database(self):
        return self.database

    def get_user(self):
        return self.user

    def get_password(self):
        return self.password
