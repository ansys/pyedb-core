"""RPC Info Utils."""

from ansys.edb.core.inner.rpc_info import rpc_information


def get_rpc_info(service_name, rpc_name):
    """Get the rpc info for the rpc corresponding to the provided service and rpc names."""
    buffered_service = rpc_information.get(service_name)
    return buffered_service.get(rpc_name) if buffered_service is not None else None


def can_cache(service_name, rpc_name):
    """Check if the response of the rpc corresponding to the provided service and rpc names can be cached."""
    if (rpc_info := get_rpc_info(service_name, rpc_name)) is not None:
        return rpc_info.can_cache
    return False


def can_buffer(service_name, rpc_name):
    """Check if the request of the rpc corresponding to the provided service and rpc names can be buffered."""
    if (rpc_info := get_rpc_info(service_name, rpc_name)) is not None:
        return rpc_info.can_buffer
    return False


def is_read(service_name, rpc_name):
    """Check if the rpc corresponding to the provided service and rpc names is a read operation."""
    if (rpc_info := get_rpc_info(service_name, rpc_name)) is not None:
        return rpc_info.is_read
    return False


def is_write(service_name, rpc_name):
    """Check if the rpc corresponding to the provided service and rpc names is a write operation."""
    if (rpc_info := get_rpc_info(service_name, rpc_name)) is not None:
        return rpc_info.is_write
    return False
