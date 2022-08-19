import os
import sys

import pytest

from ansys.edb.database import Database
from ansys.edb.session import launch_session

pyedb_path = os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..", ".."))
sys.path.append(pyedb_path)
from tests import settings
from tests.utils.filesystem import Scratch


# Wrapper class over Database
# This will ensure clean entry and exit from database
class TDatabase(object):
    def __init__(self, path: str):
        print("creating database at", path)
        self.db = Database.create(path)

    def __enter__(self):
        print("__enter__")
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__")
        self.db.save()
        self.db.close()

    def database(self):
        return self.db


class BasisTest(object):
    def setup(self):
        self.local_scratch = Scratch()
        self.s = launch_session(settings.configs.get("RPC_SERVER_ROOT"), 50051)

    def teardown(self):
        self.s.disconnect()

    def database(self, db_name: str) -> TDatabase:
        db = TDatabase(os.path.join(self.local_scratch.path, db_name))
        return db


@pytest.fixture
def runner():
    basis_test = BasisTest()
    basis_test.setup()
    yield basis_test
    basis_test.teardown()
