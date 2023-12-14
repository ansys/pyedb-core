from typing import List

from utils.fixtures import *  # noqa
from utils.test_utils import create_edb_obj_collection_msg, equals

from ansys.edb.core import database as database
from ansys.edb.core.inner.messages import bool_message, empty_message, int64_message, str_message
from ansys.edb.core.layout.cell import Cell

# Helper fixtures and functions


@pytest.fixture
def db_obj(edb_obj_msg):
    """Fixture for creating a Database used during testing.

    Returns
    -------
    Database
    """
    return database.Database(edb_obj_msg)


def _patch_database_stub(mocked_stub, test_method_name, expected_response):
    """Helper method that patches the given Database stub method with a mock server.

    Parameters
    ----------
    mocked_stub : unittest.mock.Mock
    test_method_name : str
    expected_response : Any

    Returns
    -------
    unittest.mock.Mock
    """
    mock = getattr(mocked_stub(database, database.Database), test_method_name)
    mock.return_value = expected_response
    return mock


# Tests


def test_create(random_str, edb_obj_msg, mocked_stub):
    """Test for the Database.create(db_path) method

    Parameters
    ----------
    random_str : str
        String to be used as the db_path parameter
    edb_obj_msg : EDBObjMessage
        The message that will be expected as the response from the mock server
    mocked_stub : unittest.mock.Mock
        Mocker used to patch primitive stub with the mock server
    """
    mock_server = _patch_database_stub(mocked_stub, "Create", edb_obj_msg)

    created_db = database.Database.create(random_str)

    mock_server.assert_called_once_with(str_message(random_str))

    assert isinstance(created_db, database.Database)
    assert equals(created_db.msg, edb_obj_msg)


def test_open(random_str, bool_val, edb_obj_msg, mocked_stub):
    """Test for the Database.open(db_path, read_only) method

    Parameters
    ----------
    random_str : str
        String to be used as the db_path parameter
    bool_val : bool
        Boolean to be used as the read_only parameter
    mocked_stub : unittest.mock.Mock
        Mocker used to patch primitive stub with the mock server
    """
    mock_server = _patch_database_stub(mocked_stub, "Open", edb_obj_msg)

    opened_db = database.Database.open(random_str, bool_val)

    mock_server.assert_called_once_with(
        database.database_pb2.OpenDatabaseMessage(
            edb_path=random_str,
            read_only=bool_val,
        )
    )

    assert isinstance(opened_db, database.Database)
    assert equals(opened_db.msg, edb_obj_msg)


def test_delete(random_str, bool_val, mocked_stub):
    """Test for the Database.delete(db_path) method

    Parameters
    ----------
    random_str : str
        String to be used as the db_path parameter
    bool_val : bool
        The expected return value
    mocked_stub : unittest.mock.Mock
        Mocker used to patch primitive stub with the mock server
    """
    mock_server = _patch_database_stub(mocked_stub, "Delete", empty_message())

    result = database.Database.delete(random_str)

    mock_server.assert_called_once_with(str_message(random_str))

    assert result is None


def test_save(db_obj, bool_val, mocked_stub):
    """Test for the Database.save() method

    Parameters
    ----------
    db_obj : Database
        Database to be saved
    bool_val : bool
        The expected return value
    mocked_stub : unittest.mock.Mock
        Mocker used to patch primitive stub with the mock server
    """
    mock_server = _patch_database_stub(mocked_stub, "Save", empty_message())

    result = db_obj.save()

    mock_server.assert_called_once_with(db_obj.msg)

    assert result is None


def test_close(db_obj, bool_val, mocked_stub):
    """Test for the Database.close() method

    Parameters
    ----------
    db_obj : Database
        Database to be closed
    bool_val : bool
        The expected return value
    mocked_stub : unittest.mock.Mock
        Mocker used to patch primitive stub with the mock server
    """
    mock_server = _patch_database_stub(mocked_stub, "Close", empty_message())

    expected_message = db_obj.msg
    result = db_obj.close()

    mock_server.assert_called_once_with(expected_message)

    assert result is None
    assert db_obj.is_null


@pytest.mark.parametrize("expected_num_top_cells", list(range(3)))
def test_top_circuit_cells(db_obj, expected_num_top_cells, mocked_stub):
    """Test for the Database.top_circuit_cells property

    Parameters
    ----------
    db_obj : Database
        Database to retrieve the top circuit cells of
    expected_num_top_cells : int
        The expected number of retrieved top cells
    mocked_stub : unittest.mock.Mock
        Mocker used to patch primitive stub with the mock server
    """
    expected_response = create_edb_obj_collection_msg(expected_num_top_cells)

    mock_server = _patch_database_stub(mocked_stub, "GetTopCircuits", expected_response)

    top_cells = db_obj.top_circuit_cells

    mock_server.assert_called_once_with(db_obj.msg)

    assert isinstance(top_cells, List)
    assert len(top_cells) == expected_num_top_cells
    for top_cell_idx in range(expected_num_top_cells):
        top_cell = top_cells[top_cell_idx]
        assert isinstance(top_cell, Cell)
        assert equals(top_cell.msg, expected_response.items[top_cell_idx])


def test_get_id(db_obj, random_int, mocked_stub):
    """Test for the Database.get_id() method

    Parameters
    ----------
    db_obj : Database
        Database to get the id of
    random_int : int
        The expected return value
    mocked_stub : unittest.mock.Mock
        Mocker used to patch primitive stub with the mock server
    """
    mock_server = _patch_database_stub(mocked_stub, "GetId", int64_message(random_int))

    db_id = db_obj.edb_uid

    mock_server.assert_called_once_with(db_obj.msg)

    assert db_id == random_int


def test_is_read_only(db_obj, bool_val, mocked_stub):
    """Test for the Database.is_read_only() method

    Parameters
    ----------
    db_obj : Database
        Database to get the "read only" flag of
    bool_val : bool
        The expected return value
    mocked_stub : unittest.mock.Mock
        Mocker used to patch primitive stub with the mock server
    """
    mock_server = _patch_database_stub(mocked_stub, "IsReadOnly", bool_message(bool_val))

    is_read_only = db_obj.is_read_only

    mock_server.assert_called_once_with(db_obj.msg)

    assert is_read_only == bool_val


def test_find_by_id(random_int, edb_obj_msg, mocked_stub):
    """Test for the Database.is_read_only(db_id) method

    Parameters
    ----------
    random_int : int
        Int to be used as the db_id parameter
    edb_obj_msg : EDBObjMessage
        The message that will be expected as the response from the mock server
    mocked_stub : unittest.mock.Mock
        Mocker used to patch primitive stub with the mock server
    """
    mock_server = _patch_database_stub(mocked_stub, "FindById", edb_obj_msg)

    found_db = database.Database.find_by_id(random_int)

    mock_server.assert_called_once_with(int64_message(random_int))

    assert isinstance(found_db, database.Database)
    assert equals(found_db.msg, edb_obj_msg)
