import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from apy2.core.api import Api
from apy2.connection.localconnection import CreateLocalConnector

def niceApi():  # pragma: no cover
    api = Api()

    @api.add()
    def walk():
        pass

    @api.add()
    def look():
        pass

    with api.context("home"):
        @api.add()
        def sleep():
            pass

        @api.add()
        def watch_tv():
            pass

    with api.context("work"):
        @api.add()
        def drink_coffe():
            pass

        @api.add()
        def code():
            pass
    return api


class TestLocalConnectorPartial(unittest.TestCase):  # pragma: no cover

    def setUp(self):
        self.api = niceApi()
        pool = self.api.find_functions(context="root")
        pool.extend(self.api.find_functions(context="work"))
        self.lc = CreateLocalConnector(pool)

    def test_type(self):
        from apy2.connection.localconnection import PartialLocalConnector,\
            LocalConnector
        self.assertIsInstance(self.lc, LocalConnector)
        self.assertIsInstance(self.lc, PartialLocalConnector)

    def test_details(self):
        d = self.lc.details()
#

#


class TestLocalConnectorFull(unittest.TestCase):  # pragma: no cover

    def setUp(self):
        self.api = niceApi()
        self.lc = CreateLocalConnector(self.api)

    def test_type(self):
        from apy2.connection.localconnection import FullLocalConnector,\
            LocalConnector
        self.assertIsInstance(self.lc, FullLocalConnector)
        self.assertIsInstance(self.lc, LocalConnector)

    def test_details(self):
        d = self.lc.details()
