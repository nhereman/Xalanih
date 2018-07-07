class Connection:

    def __init__(self):
        self.queries = []
        self.rowcounts = None

    def query(self, query):
        self.queries.append(query)

    def cursor(self):
        return Cursor(self,self.nextRowCount())

    def getQueries(self):
        return self.queries

    def reinit(self):
        self.queries = []

    def setResultList(self, results):
        self.results = results
    
    def setRowcountList(self, rowcounts):
        self.rowcounts = rowcounts

    def nextRowCount(self):
        if self.rowcounts == None or self.rowcounts == []:
            return None
        res = self.rowcounts[0]
        self.rowcounts = self.rowcounts[1:]
        return res

    def nextResult(self):
        res = self.results[0]
        self.results = self.results[1:]
        return res


class Cursor:

    def __init__(self,connection, rowcount):
        self.connection = connection
        self.rowcount = rowcount

    def execute(self, request, params=None):
        if params != None:
            request += str(params)
        self.connection.query(request)
        return None

    def fetchall(self):
        return self.connection.nextResult()

    def close(self):
        pass