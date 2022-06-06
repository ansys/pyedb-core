import random

from ansys.api.edb.v1.edb_messages_pb2 import EDBObjCollectionMessage, EDBObjMessage

from ansys.edb.core.models.base import ObjBase

# Comparison utils


def equals(v0, v1):
    """Checks if two values are equivalent

    Returns
    -------
    bool
    """
    if isinstance(v0, EDBObjMessage) and isinstance(v1, EDBObjMessage):
        return v0.SerializeToString() == v1.SerializeToString()
    if isinstance(v0, ObjBase) and isinstance(v1, ObjBase):
        return equals(v0.msg, v1.msg)
    raise NotImplementedError()


def generate_random_int():
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
    return EDBObjMessage(id=generate_random_int())


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


def patch_stub(stub_getter, mocker, test_method_name, expected_response, **kwargs):
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

    mocker.patch(stub_getter, return_value=mock_server, **kwargs)

    # Return the mock server
    return getattr(mock_server, test_method_name)
