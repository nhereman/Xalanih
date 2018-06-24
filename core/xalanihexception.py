class XalanihException(Exception):

    TABLE_EXISTS = 1
    NO_CREATION_SCRIPT = 2
    DB_TYPE_NOT_SUPPORTED = 3
    ALREADY_CONNECTED = 4

    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

    def getErrorCode(self):
        return self.error_code