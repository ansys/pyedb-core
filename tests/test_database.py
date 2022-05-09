from typing import List

from ansys.api.edb.v1.edb_messages_pb2 import EDBObjMessage
import pytest
import pytest_mock

from ansys.edb.core.models.cell.cell import Cell
from ansys.edb.core.models.database import Database, database_pb2
from utils.test_utils import (
    create_bool_msg,
    create_edb_obj_collection_msg,
    create_edb_obj_msgs,
    create_int64_msg,
    create_string_msg,
    msgs_are_equal,
    patch_stub,
)

# Helper fixtures and functions


@pytest.fixture(params=["edb_path_0.aedb", "edb_path_1.aedb"])
def db_path(request):
    return request.param


@pytest.fixture(params=[Database(msg) for msg in create_edb_obj_msgs(2)])
def db_obj(request):
    return request.param


def _patch_database_stub(
    mocker: pytest_mock.MockerFixture, test_method_name: str, expected_request, expected_response
):
    patch_stub(
        "ansys.edb.core.models.database.get_database_stub",
        mocker,
        test_method_name,
        expected_request,
        expected_response,
    )


# Tests


def test_create(db_path: str, edb_obj_msg: EDBObjMessage, mocker):
    expected_request = create_string_msg(db_path)

    _patch_database_stub(mocker, "Create", expected_request, edb_obj_msg)

    created_db = Database.create(db_path)
    assert isinstance(created_db, Database)
    assert msgs_are_equal(created_db._msg, edb_obj_msg)


def test_open(db_path: str, bool_val: bool, edb_obj_msg: EDBObjMessage, mocker):
    expected_request = database_pb2.OpenDatabaseMessage(
        edb_path=create_string_msg(db_path),
        read_only=create_bool_msg(bool_val),
    )

    _patch_database_stub(mocker, "Open", expected_request, edb_obj_msg)

    opened_db = Database.open(db_path, bool_val)
    assert isinstance(opened_db, Database)
    assert msgs_are_equal(opened_db._msg, edb_obj_msg)


def test_delete(db_path: str, bool_val: bool, mocker):
    expected_request = create_string_msg(db_path)
    expected_response = create_bool_msg(bool_val)

    _patch_database_stub(mocker, "Delete", expected_request, expected_response)

    assert Database.delete(db_path) == bool_val


def test_save(db_obj: Database, bool_val: bool, mocker):
    expected_response = create_bool_msg(bool_val)

    _patch_database_stub(mocker, "Save", db_obj._msg, expected_response)

    assert db_obj.save() == bool_val


def test_close(db_obj: Database, bool_val: bool, mocker):
    expected_response = create_bool_msg(bool_val)

    _patch_database_stub(mocker, "Close", db_obj._msg, expected_response)

    assert db_obj.close() == bool_val


@pytest.mark.parametrize("expected_num_top_cells", list(range(3)))
def test_top_circuit_cells(db_obj: Database, expected_num_top_cells: int, mocker):
    expected_response = create_edb_obj_collection_msg(expected_num_top_cells)

    _patch_database_stub(mocker, "GetTopCircuits", db_obj._msg, expected_response)

    top_cells = db_obj.top_circuit_cells
    assert isinstance(top_cells, List)
    assert len(top_cells) == expected_num_top_cells
    for top_cell_idx in range(expected_num_top_cells):
        top_cell = top_cells[top_cell_idx]
        assert isinstance(top_cell, Cell)
        assert msgs_are_equal(top_cell._msg, expected_response.edb_obj_collection[top_cell_idx])


def test_get_id(db_obj: Database, edb_obj_id: int, mocker):
    expected_response = create_int64_msg(edb_obj_id)

    _patch_database_stub(mocker, "GetId", db_obj._msg, expected_response)

    assert db_obj.get_id() == edb_obj_id


def test_is_read_only(db_obj: Database, bool_val: bool, mocker):
    expected_response = create_bool_msg(bool_val)

    _patch_database_stub(mocker, "IsReadOnly", db_obj._msg, expected_response)

    assert db_obj.is_read_only() == bool_val


def test_find_by_id(edb_obj_id: int, edb_obj_msg: EDBObjMessage, mocker):
    expected_request = create_int64_msg(edb_obj_id)

    _patch_database_stub(mocker, "FindById", expected_request, edb_obj_msg)

    found_db = Database.find_by_id(edb_obj_id)
    assert isinstance(found_db, Database)
    assert msgs_are_equal(found_db._msg, edb_obj_msg)
