import pytest

from ansys.edb.database import Database
from ansys.edb.layout import Cell, CellType
from ansys.edb.session import launch_session
import settings


@pytest.fixture(scope="module")
def session():
    with launch_session(settings.configs.get("RPC_SERVER_ROOT"), 50051):
        yield


@pytest.fixture
def database_path(tmp_path):
    return str(tmp_path / "test.aedb")


@pytest.fixture
def database(session, database_path):
    db = Database.create(database_path)
    yield db
    db.close()


@pytest.fixture
def circuit_cell(database):
    return Cell.create(database, CellType.CIRCUIT_CELL, "circuit_cell")
