class DBConnector:
    
    def connect(self):
        raise Exception("DbConnector-connect: DbConnector is abstract and \
                            should not be called directly")

    def getConnection(self):
        raise Exception("DbConnector-getConnection: DbConnector is abstract \
                            and should not be called directly")