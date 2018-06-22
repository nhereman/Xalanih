from core.requesthandler import RequestHandler

class MysqlRequestHandler(RequestHandler):

    def requestXalanihTable(self):
        return "SHOW TABLES like 'xalanih_updates'"

    def requestXalanihTableCreation(self):
        return ("CREATE TABLE xalanih_updates ("
                "`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                "`update_name` VARCHAR(150) NOT NULL,"
                "`update_apply_time` TIME NOT NULL,"
                "PRIMARY KEY (`id`));")

    def requestUpdateRecording(self):
        return "INSERT INTO xalanih_updates \
                    (`update_name`, `update_apply_time`) \
                    VALUES (%s, NOW())"
    
    def requestUpdate(self):
        return "SELECT * FROM xalanih_updates WHERE update_name = %s"