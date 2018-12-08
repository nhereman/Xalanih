import unittest
import os
import logging
from xalanih.core.logger import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.test_file = "tst_logger"
        self.test_error = "tst_error"
        self.test_warning = "tst_warning"
        self.test_info = "tst_info"
        self.test_debug = "tst_debug"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_file_logging(self):
        logger = Logger(self.test_file, 0)

        logger.error(self.test_error)
        logger.warning(self.test_warning)
        logger.info(self.test_info)
        logger.debug(self.test_debug)

        file = open(self.test_file)
        content = file.read()
        file.close()

        self.assertTrue(self.test_error in content, "Failed error logging")
        self.assertTrue(self.test_warning in content, "Failed warning logging")
        self.assertTrue(self.test_info in content, "Failed info logging")
        self.assertTrue(self.test_debug in content, "Failed debug logging")

        # There are two handlers (file + terminal)
        self.assertEquals(len(logger.python_logger.handlers), 2)

        # Clean handlers for next test
        logger.shutdown()
        handler1=logger.python_logger.handlers[0]
        handler2=logger.python_logger.handlers[1]
        logger.python_logger.removeHandler(handler1)
        logger.python_logger.removeHandler(handler2)

    def test_no_file(self):
        logger = Logger(None, 0)

        # Only terminal handler
        self.assertEquals(len(logger.python_logger.handlers), 1)
        
        logger.shutdown()
        handler = logger.python_logger.handlers[0]
        logger.python_logger.removeHandler(handler)

    def test_verbosity(self):
        self.check_verbosity(0, 60)
        self.check_verbosity(1, logging.ERROR)
        self.check_verbosity(2, logging.WARNING)
        self.check_verbosity(3, logging.INFO)
        self.check_verbosity(4, logging.DEBUG)
        self.check_verbosity(5, logging.INFO)

    def check_verbosity(self, verbosity, level):
        logger = Logger(None, verbosity)
        self.assertEquals(logger.python_logger.handlers[0].level, level)
        logger.shutdown()
        handler = logger.python_logger.handlers[0]
        logger.python_logger.removeHandler(handler)



