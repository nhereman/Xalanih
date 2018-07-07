class Connection:

    def __init__(self):
        self.queries = []

    def query(self, query):
        self.queries.append(query)

    def cursor(self):
        return Cursor(self)

    def getQueries(self):
        return self.queries

    def reinit(self):
        self.queries = []

    def setResultList(self, results):
        self.results = results

    def nextResult(self):
        res = self.results[0]
        self.results = self.results[1:]
        return res


class Cursor:

    def __init__(self,connection):
        self.connection = connection

    def execute(self, request, params=None):
        if params != None:
            request += str(params)
        self.connection.query(request)
        return None

    def fetchall(self):
        return self.connection.nextResult()

    def close(self):
        pass