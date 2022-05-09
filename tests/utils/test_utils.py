from typing import List

from ansys.api.edb.v1.edb_messages_pb2 import EDBObjCollectionMessage, EDBObjMessage
from google.protobuf.wrappers_pb2 import BoolValue, Int64Value, StringValue
import pytest
import pytest_mock

# Comparison utils


def msgs_are_equal(msg0, msg1) -> bool:
    return msg0.SerializeToString() == msg1.SerializeToString()


# Msg Utils


def _create_edb_obj_msg() -> EDBObjMessage:
    try:
        _create_edb_obj_msg.id += 1
    except AttributeError:
        _create_edb_obj_msg.id = 1
    return EDBObjMessage(impl_ptr_address=_create_edb_obj_msg.id)


def create_edb_obj_msgs(num_msgs: int) -> List[EDBObjMessage]:
    return [_create_edb_obj_msg() for _ in range(num_msgs)]


def create_edb_obj_collection_msg(num_msgs: int) -> EDBObjCollectionMessage:
    return EDBObjCollectionMessage(edb_obj_collection=create_edb_obj_msgs(num_msgs))


def create_bool_msg(value: bool) -> BoolValue:
    return BoolValue(value=value)


def create_string_msg(value: str) -> StringValue:
    return StringValue(value=value)


def create_int64_msg(value: int) -> Int64Value:
    return Int64Value(value=value)


# Mock server utils


def _generate_mock_server_checker(expected_request, expected_response):
    def assert_expected_request(received_request):
        assert msgs_are_equal(expected_request, received_request)
        return expected_response

    return assert_expected_request


class _MockServer:
    def __init__(self, method_name: str, expected_request, expected_response):
        setattr(
            self, method_name, _generate_mock_server_checker(expected_request, expected_response)
        )


def get_mock_server(method_name: str, expected_request, expected_response):
    def mock_server_creator() -> _MockServer:
        return _MockServer(method_name, expected_request, expected_response)

    return mock_server_creator


def patch_stub(
    stub_getter: str,
    mocker: pytest_mock.MockerFixture,
    test_method_name: str,
    expected_request,
    expected_response,
):
    mocker.patch(
        stub_getter,
        get_mock_server(test_method_name, expected_request, expected_response),
    )


# Fixtures


@pytest.fixture(params=[True, False])
def bool_val(request) -> bool:
    return request.param


@pytest.fixture(params=create_edb_obj_msgs(2))
def edb_obj_msg(request) -> EDBObjMessage:
    return request.param


@pytest.fixture(params=[edb_obj_id for edb_obj_id in range(2)])
def edb_obj_id(request) -> int:
    return request.param
