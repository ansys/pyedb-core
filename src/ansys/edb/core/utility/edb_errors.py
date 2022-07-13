"""edb specific errors."""

from functools import wraps

from grpc import StatusCode
from grpc._channel import _InactiveRpcError, _MultiThreadedRendezvous

from ansys.edb.core.utility import LOGGER


def handle_grpc_exception(func):
    """Capture gRPC exceptions and return a more succinct error message."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Capture gRPC exceptions."""
        try:
            out = func(*args, **kwargs)
        except (_InactiveRpcError, _MultiThreadedRendezvous) as error:

            code = error.args[0].code
            msg = error.args[0].details
            if code == StatusCode.UNAVAILABLE:
                msg = "Cannot communicate with EDB Server"

            LOGGER.error(msg)
            # rethrow the exception
            raise
        return out

    return wrapper
