import unittest
import threading
from urllib.request import urlopen

from apy2.server.cluster_server import ClusterServer


class ThreadRunner(threading.Thread):

    def __init__(self, foo):
        threading.Thread.__init__(self)
        self.foo = foo

    def run(self):
        self.foo()

pool = []


def run_server(s):
    t = ThreadRunner(lambda: s.serve_forever())
    t.start()
    s._______deamon = t
    pool.append(s)


def stop_server(s):
    s.shutdown()
    s._______deamon.join()
    pool.remove(s)

port = 9999
url = ""


class TestClusterServer(unittest.TestCase):  # pragma: no coverimport unittest

    def setUp(self):
        global port, url
        port += 1
        url = "http://localhost:" + str(port) + "/"

    def test_run_empty(self):
        s = ClusterServer(port=port)
        run_server(s)
        r = urlopen(url + "eggs?A=12&B=asereje", timeout=1)
        self.assertEqual(r.status, 200)
        stop_server(s)

    def test_run_empty2(self):
        s = ClusterServer(port=port)
        run_server(s)
        r = urlopen(url, timeout=1)
        self.assertEqual("ASDASDASDASDF", r.read().decode("UTF-8"))
        stop_server(s)

    def tearDown(self):
        for s in pool:
            s.shutdown()
