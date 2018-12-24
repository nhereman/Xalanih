import unittest
import os
from xalanih.core.dbupdator import DBUpdator
from xalanih.core.constants import Constants
from xalanih.core.xalanihexception import XalanihException
from xalanih.core.mysql.mysqlrequesthandler import MysqlRequestHandler
from xalanih.test.mocks.connection import Connection
from xalanih.test.mocks.logger import Logger
from xalanih.test.mocks.dbchecker import DBChecker


class TestDBUpdatorMySQL(unittest.TestCase):

    def setUp(self):
        self.connection = Connection()
        self.logger = Logger()
        self.dir = os.path.dirname(__file__) + "/data/"
        self.req_handler = MysqlRequestHandler()
        self.dbupdator = DBUpdator(self.dir, self.connection, self.req_handler, self.logger)

    def tearDown(self):
        self.connection.reinit()
        self.dbupdator = None

    def test_apply_updatesNoTable(self):
        checker = DBChecker(exists=False)

        self.connection.set_result_list([()])
        with self.assertRaises(XalanihException) as cm:
            self.dbupdator.apply_updates(checker, None)
        self.assertEqual(XalanihException.TABLE_NOT_FOUND,
                         cm.exception.get_error_code(),
                         "Wrong error code.")

    def test_apply_updatesNoUpdates(self):
        checker = DBChecker(exists=True)

        self.connection.set_result_list([])
        self.dir += "creation_test"
        self.dbupdator = DBUpdator(self.dir, self.connection, self.req_handler, self.logger)
        self.dbupdator.apply_updates(checker, None)
        queries = self.connection.get_queries()
        self.assertEqual(0, len(queries))

    def test_apply_updatesSuccess(self):
        checker = DBChecker(exists=True)

        self.dir += "update_test"
        inc_updates = self.getListofIncludedUpdates()
        updates = self.getListOfUpdates()

        self.connection.set_result_list([((Constants.XALANIH_TABLE,),)])
        self.connection.set_rowcount_list(
                        [(1 if i < len(inc_updates) else 0) for i in range(5)])
        self.dbupdator = DBUpdator(self.dir, self.connection, self.req_handler, self.logger)
        self.dbupdator.apply_updates(checker, None)

        queries = self.connection.get_queries()
        expected_queries = len(updates) + 2*(len(updates)-len(inc_updates))
        self.assertEqual(expected_queries, len(queries),
                         "Not the expected number of queries")

        for update in inc_updates:
            self.assertEqual(1, self.getNbRequested(queries, update),
                             "Wrong amount of request linked to" 
                             " the included update: {0}".format(update))
        
        for update in [u for u in updates if u not in inc_updates]:
            self.assertEqual(2, self.getNbRequested(queries, update),
                             "Wrong amount of request linked to" 
                             " the update: {0}".format(update))

    def test_apply_updatesLastUpdateSuccess(self):
        checker = DBChecker(exists=True)

        self.dir += "update_test"
        inc_updates = self.getListofIncludedUpdates()
        updates = self.getListOfUpdates()
        last_update = updates[-2]

        self.connection.set_result_list([])
        self.connection.set_rowcount_list(
                        [(1 if i < len(inc_updates) else 0) for i in range(5)])
        self.dbupdator = DBUpdator(self.dir, self.connection, self.req_handler, self.logger)
        self.dbupdator.apply_updates(checker, last_update)

        queries = self.connection.get_queries()
        expected_queries = (len(updates)-1) + 2*(len(updates)-len(inc_updates)-1)
        self.assertEqual(expected_queries, len(queries),
                         "Not the expected number of queries")

        for update in inc_updates:
            self.assertEqual(1, self.getNbRequested(queries, update),
                             "Wrong amount of request linked to" 
                             " the included update: {0}".format(update))
        
        for update in [u for u in updates if u not in inc_updates and u <= last_update]:
            self.assertEqual(2, self.getNbRequested(queries, update),
                             "Wrong amount of request linked to" 
                             " the update: {0}".format(update))

    def test_apply_updatesLastUpdateNotExist(self):
        checker = DBChecker(exists=True)

        self.dir += "update_test"
        last_update = "INVALID_UPDATE"
        self.connection.set_result_list([((Constants.XALANIH_TABLE,),)])
        self.dbupdator = DBUpdator(self.dir, self.connection, self.req_handler, self.logger)
        with self.assertRaises(XalanihException) as cm:
            self.dbupdator.apply_updates(checker, last_update)
        self.assertEqual(XalanihException.UPDATE_NOT_FOUND,
                         cm.exception.get_error_code(),
                         "Wrong error code.")

    def test_apply_updatesLastUpdateInIncluded(self):
        checker = DBChecker(exists=True)

        self.dir += "update_test"
        inc_updates = self.getListofIncludedUpdates()
        updates = self.getListOfUpdates()
        last_update = inc_updates[0]

        self.connection.set_result_list([()])
        self.connection.set_rowcount_list(
                        [(1 if i <= len(inc_updates) else 0) for i in range(5)])
        self.dbupdator = DBUpdator(self.dir, self.connection, self.req_handler, self.logger)
        self.dbupdator.apply_updates(checker, last_update)

        queries = self.connection.get_queries()
        self.assertEqual(1, len(queries),
                         "Not the expected number of queries")

        self.assertEqual(1, self.getNbRequested(queries, last_update),
                         "Wrong amount of request linked to" 
                         " the included update: {0}".format(last_update))
        
        for update in [u for u in updates if u != last_update]:
            self.assertEqual(0, self.getNbRequested(queries, update),
                             "Wrong amount of request linked to" 
                             " the update: {0}".format(update))

    def getListOfUpdates(self):
        directory = self.dir + "/" + Constants.DIR_UPDATE
        files = os.listdir(directory)
        res = [f[:-4] for f in files if f.endswith(".sql")]
        res.sort()
        return res

    def getListofIncludedUpdates(self):
        incfile = open(self.dir + "/" + Constants.PATH_INC_UPDATES)
        lines = incfile.readlines()
        incfile.close()
        return [l.strip() for l in lines]

    @staticmethod
    def getNbRequested(queries, update):
        count = 0
        for q in queries:
            if q.find(update.strip()) != -1:
                count += 1
        return count
