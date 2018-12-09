import unittest

from xalanih.core.dbchecker import DBChecker
from xalanih.core.mysql.mysqlrequesthandler import MysqlRequestHandler
from xalanih.core.xalanihexception import XalanihException
from xalanih.core.constants import Constants
from xalanih.test.mocks.connection import Connection
from xalanih.test.mocks.logger import Logger


class TestDBCheckerMysql(unittest.TestCase):

    def setUp(self):
        self.connection = Connection()
        self.logger = Logger()
        self.req_handler = MysqlRequestHandler()
        self.checker = DBChecker(self.connection, self.req_handler, self.logger)

    def tearDown(self):
        self.connection.reinit()
        self.checker = None

    def test_last_update(self):
        self.connection.set_result_list([((Constants.XALANIH_TABLE,),), ("tst_update",)])
        result = self.checker.check_last_update()
        self.assertEquals(result, "tst_update")

    def test_last_update_no_table(self):
        self.connection.set_result_list([()])
        with self.assertRaises(XalanihException) as e:
            self.checker.check_last_update()
        self.assertEquals(e.exception.getErrorCode(),
                          XalanihException.TABLE_NOT_FOUND,
                          "Wrong error code.")