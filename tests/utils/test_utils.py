import random
import string

from ansys.api.edb.v1.edb_messages_pb2 import EDBObjCollectionMessage, EDBObjMessage
import pytest

# Comparison utils


def msgs_are_equal(msg0, msg1):
    """Checks if two messages are equivalent by serializing them to strings and comparing them

    Returns
    -------
    bool
    """
    return msg0.SerializeToString() == msg1.SerializeToString()


# Private utils


def _generate_random_int():
    """Generates a random integer between 0 and 100,000. Note this is not guaranteed to be unique.

    Returns
    -------
    int
    """
    return random.randint(0, 100000)


# Msg utils


def create_edb_obj_msg():
    """Creates and EDBObjMessage where the id is a random number

    Returns
    -------
    EDBObjMessage
    """
    return EDBObjMessage(id=_generate_random_int())


def create_edb_obj_msgs(num_msgs):
    """Creates a list of EDBObjMessages

    Parameters
    ----------
    num_msgs : int
        number of EDBObjMessages to create

    Returns
    -------
    List[EDBObjMessage]
    """
    return [create_edb_obj_msg() for _ in range(num_msgs)]


def create_edb_obj_collection_msg(num_msgs):
    """Creates an EDBObjCollectionMessage

    Parameters
    ----------
    num_msgs : int
        number of EDBObjMessages to store in the EDBObjCollectionMessage

    Returns
    -------
    EDBObjCollectionMessage
    """
    return EDBObjCollectionMessage(edb_obj_collection=create_edb_obj_msgs(num_msgs))


# Mock server utils


def patch_stub(stub_getter, mocker, test_method_name, expected_response):
    """Helper method that patches the given stub method.

    Parameters
    ----------
    stub_getter : str
        Module path to stub getter method
    mocker : pytest_mock.MockerFixture
        Mocker fixture used when patching the stub method
    test_method_name : str
        Name of stub method to be patched
    expected_response : Any
        The response message that will be returned by the mocked stub method
    Returns
    -------
    unittest.mock.Mock
    """

    # Create the mock server
    mock_server = mocker.Mock()
    mock_server_attr = {test_method_name + ".return_value": expected_response}
    mock_server.configure_mock(**mock_server_attr)

    # Patch the stub getter method with the mock server
    mocker.patch(
        stub_getter,
        return_value=mock_server,
    )

    # Return the mock server
    return getattr(mock_server, test_method_name)


# Fixtures


@pytest.fixture(params=[True, False])
def bool_val(request):
    """Parameterized fixture that returns True and False values

    Returns
    -------
    bool
    """
    return request.param


@pytest.fixture
def edb_obj_msg():
    """Fixture for creating an EDBObjMessage.

    Returns
    -------
    EDBObjMessage
    """
    return create_edb_obj_msg()


@pytest.fixture
def random_str():
    """Fixture for creating a 10 character long string comprised of random ascii letters.

    Returns
    -------
    str
    """
    return "".join(random.choice(string.ascii_letters) for _ in range(10))


@pytest.fixture
def random_int():
    """Fixture for generating a random integer between 0 and 100,000.

    Returns
    -------
    int
    """
    return _generate_random_int()
