from core.requesthandler import RequestHandler
from core.constants import Constants


class MysqlRequestHandler(RequestHandler):

    def requestXalanihTable(self):
        return "SHOW TABLES like '{0}'".format(Constants.XALANIH_TABLE)

    def requestXalanihTableCreation(self):
        return ("CREATE TABLE {0} ("
                "`{1}` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                "`{2}` VARCHAR(150) NOT NULL,"
                "`{3}` TIME NOT NULL,"
                "PRIMARY KEY (`{1}`));").format(Constants.XALANIH_TABLE,
                                                Constants.COL_ID,
                                                Constants.COL_UPDT_NAME,
                                                Constants.COL_UPDT_TIME)

    def requestUpdateRecording(self):
        return ("INSERT INTO {0} "
                "(`{1}`, `{2}`) "
                "VALUES (%s, NOW())").format(Constants.XALANIH_TABLE,
                                                Constants.COL_UPDT_NAME,
                                                Constants.COL_UPDT_TIME)
    
    def requestUpdate(self):
        return "SELECT * FROM {0} WHERE {1} = %s".format(
                                                Constants.XALANIH_TABLE,
                                                Constants.COL_UPDT_NAME)