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
        return "1"

    @api.add()
    def look():
        return 2

    with api.context("home"):
        @api.add()
        def sleep():
            return 3.1

        @api.add()
        def watch_tv():
            return 400000000

    with api.context("work"):
        @api.add()
        def drink_coffe():
            return {"5": 5}

        @api.add()
        def code():
            return ["6", "6", "6"]
    return api


class TestLocalContextConnector(unittest.TestCase):  # pragma: no cover

    def setUp(self):
        self.api = niceApi()
        self.lcroot = CreateLocalConnector(self.api.context("root"))
        self.lcwork = CreateLocalConnector(self.api.context("work"))
        self.lchome = CreateLocalConnector(self.api.context("home"))

    def test_type(self):
        from apy2.connection.localconnection import ContextConnector,\
            LocalContextConnector
        self.assertIsInstance(self.lcroot, ContextConnector)
        self.assertIsInstance(self.lcroot, LocalContextConnector)
        self.assertIsInstance(self.lcwork, ContextConnector)
        self.assertIsInstance(self.lcwork, LocalContextConnector)

    # remote rpc function will be /__details?
    def test_details(self):
        d = self.lcwork.details()
        self.assertEqual("context", d["cluster_type"])

    def test_works_like_context(self):
        with self.lcroot as c:
            self.assertEqual(c.walk(), "1")
            self.assertEqual(c.look(), 2)
        with self.lchome as c:
            self.assertEqual(c.sleep(), 3.1)
            self.assertEqual(c.watch_tv(), 400000000)
        with self.lcwork as c:
            self.assertEqual(c.drink_coffe(), {"5": 5})
            self.assertEqual(c.code(), ["6", "6", "6"])

    def test_can_call_get_foo_to_retrive_function(self):
        f = self.lcroot.get_function("look")
        self.assertEqual(2, f())

    def test_no_foo_exception_is_properly_named(self):
        with self.assertRaisesRegex(Exception,
                                    "Context do not have function *"):
            self.lcwork.get_function("sleep")

        with self.assertRaisesRegex(Exception,
                                    "Context do not have function *"):
            with self.lchome as c:
                c.drink_coffe()

    # remote rpc function will be /__list?
    def test_list_functions(self):
        l = self.lcroot.list_functions()
        self.assertEqual(2, len(l))
        self.assertIn("look", l)
        self.assertIn("walk", l)

#

#


# class TestLocalConnectorFull(unittest.TestCase):  # pragma: no cover

#     def setUp(self):
#         self.api = niceApi()
#         self.lc = CreateLocalConnector(self.api)

#     def test_type(self):
#         from apy2.connection.localconnection import FullLocalConnector,\
#             LocalConnector
#         self.assertIsInstance(self.lc, FullLocalConnector)
#         self.assertIsInstance(self.lc, LocalConnector)

#     def test_details(self):
#         d = self.lc.details()
