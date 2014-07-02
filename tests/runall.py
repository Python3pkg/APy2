import unittest
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from api import *
from localconnection import *
from responses import *
from cluster_server import *

if __name__ == "__main__":
    unittest.main(warnings='ignore')
