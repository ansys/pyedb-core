"""EDB Error Manager."""

from enum import Enum
from typing import List

import ansys.api.edb.v1.edb_error_manager_pb2 as pb2
from ansys.api.edb.v1.edb_error_manager_pb2_grpc import EDBErrorManagerServiceStub
import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core.inner.utils import stream_items_from_server
from ansys.edb.core.session import StubAccessor, StubType

__stub_accessor = StubAccessor(StubType.edb_error_manager)


def _get_stub() -> EDBErrorManagerServiceStub:
    return __stub_accessor.__get__()


class EDBErrorSeverity(Enum):
    """Enum representing the severity of an :class:`.EDBError`."""

    INFO = pb2.EDBErrorSeverity.INFO
    WARNING = pb2.EDBErrorSeverity.WARNING
    ERROR = pb2.EDBErrorSeverity.ERROR
    FATAL = pb2.EDBErrorSeverity.FATAL


class EDBError:
    """Class representing an error received from the EDB error manager on the server."""

    def __init__(self, message: str, severity: EDBErrorSeverity):
        """Construct an EDBError object.

        Parameters
        ----------
        message : str
        severity : .EDBErrorSeverity
        """
        self._message = message
        self._severity = severity

    @property
    def message(self) -> str:
        """:obj:`str`: The message stored in the error."""
        return self._message

    @property
    def severity(self) -> EDBErrorSeverity:
        """:class:`.EDBErrorSeverity`: The severity of the error."""
        return self._severity


def _msg_to_edb_error(msg):
    return EDBError(msg.message, EDBErrorSeverity(msg.severity))


def get_error_messages() -> List[EDBError]:
    """Get all the error messages stored in the EDB error manager. All existing \
    messages in the EDB error manager are cleared.

    Returns
    -------
    list of .EDBError
    """
    return stream_items_from_server(
        _msg_to_edb_error, _get_stub().GetErrors(empty_pb2.Empty()), "messages"
    )
