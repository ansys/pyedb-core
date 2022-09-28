import pytest
import settings

from ansys.edb.database import Database
from ansys.edb.layout import Cell, CellType
from ansys.edb.session import session


@pytest.fixture
def test_session():
    with session(settings.configs.get("RPC_SERVER_ROOT"), 50051):
        yield


@pytest.fixture
def new_database_path(tmp_path):
    return str(tmp_path / "test.aedb")


@pytest.fixture
def new_database(test_session, new_database_path):
    db = Database.create(new_database_path)
    yield db
    db.close()


@pytest.fixture
def circuit_cell(new_database):
    return Cell.create(new_database, CellType.CIRCUIT_CELL, "circuit_cell")
