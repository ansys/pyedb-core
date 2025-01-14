"""Cache."""

from contextlib import contextmanager
from sys import modules

from ansys.api.edb.v1.caching_pb2 import BufferEntryMessage, BufferMessage, FutureMessage
from django.utils.module_loading import import_string
from google.protobuf.any_pb2 import Any
from google.protobuf.empty_pb2 import Empty

# The cache module singleton
MOD = modules[__name__]
MOD.io_manager = None

_buffered_rpcs = {"ansys.api.edb.v1.RectangleService": {"Create": True}}

_future_id = 1


def _get_next_future_id():
    global _future_id
    _future_id += 1
    return _future_id


class _CacheOutcome:
    def __init__(self, result):
        self._result = result

    def result(self):
        return self._result


class _Cache:
    def __init__(self):
        self._response_cache = {}
        self._msg_type_cache = {}

    def _extract_msg_from_any_module_msg(self, any_module_msg):
        msg_type_name = any_module_msg.any.TypeName()
        msg_type = self._msg_type_cache.get(msg_type_name)
        if msg_type is None:
            insertion_idx = msg_type_name.rindex(".")
            msg_class_path = (
                msg_type_name[: insertion_idx + 1]
                + any_module_msg.module
                + "_pb2"
                + msg_type_name[insertion_idx:]
            )
            msg_type = import_string(msg_class_path)
            self._msg_type_cache[msg_type_name] = msg_type
        msg = msg_type()
        any_module_msg.any.Unpack(msg)
        return msg

    @staticmethod
    def _generate_cache_key(service_name, rpc_method_name, request):
        """Generate a unique cache key based on the request."""
        return f"{service_name}-{rpc_method_name}-{str(request)}"

    def add(self, service_name, rpc_method_name, request_msg, response_msg):
        key = self._generate_cache_key(service_name, rpc_method_name, request_msg)
        self._response_cache[key] = _CacheOutcome(response_msg)

    def add_from_cache_msg(self, cache_msg):
        for cache_entry in cache_msg.cache:
            request_msg = self._extract_msg_from_any_module_msg(cache_entry.request)
            response_msg = self._extract_msg_from_any_module_msg(cache_entry.response)
            self.add(
                cache_entry.service_name, cache_entry.rpc_method_name, request_msg, response_msg
            )
        if cache_msg.cache:
            cache_msg.ClearField("cache")

    def get(self, service_name, rpc_method_name, request_msg):
        return self._response_cache.get(
            self._generate_cache_key(service_name, rpc_method_name, request_msg)
        )


class _Buffer:
    class _BufferEntry:
        def __init__(self, service_name, rpc_name, request, future_id):
            self._service_name = service_name
            self._rpc_name = rpc_name
            self._request = request
            self._future_id = future_id

        def msg(self):
            any_request = Any()
            any_request.Pack(self._request)
            msg = BufferEntryMessage(
                service_name=self._service_name, rpc_name=self._rpc_name, request=any_request
            )
            if self._future_id is not None:
                msg.future_id = self._future_id
            return msg

    def __init__(self):
        self._reset()

    def _reset(self):
        self._buffer = []
        self._futures = {}
        self._is_flushing = False

    def add_request(self, service_name, rpc_name, request):
        buffered_service = _buffered_rpcs.get(service_name)
        if buffered_service is None:
            return
        buffered_rpc_returns_future = buffered_service.get(rpc_name)
        if buffered_rpc_returns_future is None:
            return
        future_id = _get_next_future_id() if buffered_rpc_returns_future else None
        self._buffer.append(self._BufferEntry(service_name, rpc_name, request, future_id))
        return _CacheOutcome(Empty if future_id is None else FutureMessage(id=future_id))

    def flush(self):
        if not self._buffer:
            return
        from ansys.edb.core.session import StubAccessor, StubType

        stub = StubAccessor(StubType.caching).__get__()
        request = BufferMessage(buffer=[buffer_entry.msg() for buffer_entry in self._buffer])
        with self._begin_flush():
            response = stub.FlushBuffer(request)
            for future in response.resolved_futures:
                self._futures[future.future_id].msg = future.edb_obj

    def add_future_ref(self, future):
        self._futures[future.id(False)] = future

    @property
    def is_flushing(self):
        return self._is_flushing

    @contextmanager
    def _begin_flush(self):
        try:
            self._is_flushing = True
            yield
        finally:
            self._reset()


class _IOManager:
    def __init__(self):
        self._cache = _Cache()
        self._buffer = _Buffer()

    @property
    def cache(self):
        """Get the active cache."""
        return self._cache

    @property
    def buffer(self):
        """Get the active buffer."""
        return self._buffer


@contextmanager
def enable_io_manager():
    """Enable caching of data from the server for code called within the context manager and improve performance of \
    read-only operations.

    .. note::
        This is intended for use with read-only operations. If modifications are made to the EDB in this code block, \
        the changes will not be reflected when querying the server until after the context manager is exited.
    """
    try:
        MOD.io_manager = _IOManager()
        yield
    finally:
        MOD.io_manager = None


def get_io_manager():
    """Get the active IO manager."""
    return MOD.io_manager


def get_cache():
    """Get the active cache."""
    return MOD.io_manager.cache if MOD.io_manager is not None else None


def get_buffer():
    """Get the active buffer."""
    return MOD.io_manager.buffer if MOD.io_manager is not None else None
