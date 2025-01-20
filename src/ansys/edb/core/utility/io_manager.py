"""Cache."""

from contextlib import contextmanager
from enum import Enum, auto
from sys import modules

from ansys.api.edb.v1.caching_pb2 import BufferEntryMessage, BufferMessage
from ansys.api.edb.v1.edb_messages_pb2 import EDBObjCollectionMessage, EDBObjMessage
from django.utils.module_loading import import_string
from google.protobuf.any_pb2 import Any
from google.protobuf.empty_pb2 import Empty

# The cache module singleton
MOD = modules[__name__]

_buffered_rpcs = {
    "ansys.api.edb.v1.RectangleService": {"Create": True},
    "ansys.api.edb.v1.PrimitiveService": {"SetIsNegative": True},
}

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
        self._is_enabled = True
        self._cached_edb_objs = {}
        self._active_edb_objs_to_refresh = []
        self._is_refreshing = False

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
        # TODO: check if service/rpc is tagged as cacheable
        key = self._generate_cache_key(service_name, rpc_method_name, request_msg)
        self._response_cache[key] = _CacheOutcome(response_msg)

    def add_from_cache_msg(self, edb_obj_msg):
        cache_msg = edb_obj_msg.cache
        for cache_entry in cache_msg.cache:
            request_msg = self._extract_msg_from_any_module_msg(cache_entry.request)
            response_msg = self._extract_msg_from_any_module_msg(cache_entry.response)
            self.add(
                cache_entry.service_name, cache_entry.rpc_method_name, request_msg, response_msg
            )
            self._cached_edb_objs[edb_obj_msg.id] = True
        if cache_msg.cache:
            cache_msg.ClearField("cache")

    def get(self, service_name, rpc_method_name, request_msg):
        return self._response_cache.get(
            self._generate_cache_key(service_name, rpc_method_name, request_msg)
        )

    def invalidate(self):
        if not self._response_cache:
            return
        self._response_cache.clear()
        self._cached_edb_objs = self._cached_edb_objs.fromkeys(self._cached_edb_objs, False)
        get_io_manager().add_notification_for_server(ServerNotification.INVALIDATE_CACHE)

    def add_active_edb_obj(self, edb_obj_msg):
        self._active_edb_objs_to_refresh.append(edb_obj_msg)

    def refresh_for_request(self):
        if not self._active_edb_objs_to_refresh:
            return

        from ansys.edb.core.session import StubAccessor, StubType

        edb_objs_to_refresh = [
            edb_obj_msg
            for edb_obj_msg in self._active_edb_objs_to_refresh
            if self._cached_edb_objs.get(edb_obj_msg.id) is False
        ]
        if not edb_objs_to_refresh:
            return
        stub = StubAccessor(StubType.caching).__get__()
        with self._begin_refresh():
            response = stub.RefreshCache(EDBObjCollectionMessage(items=edb_objs_to_refresh))
            for msg in response.items:
                self.add_from_cache_msg(msg)
            self._active_edb_objs_to_refresh.clear()

    @property
    def is_refreshing(self):
        return self._is_refreshing

    @contextmanager
    def _begin_refresh(self):
        try:
            self._is_refreshing = True
            yield
        finally:
            self._is_refreshing = False


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
        self._active_future_requests = {}
        self._is_flushing = False

    def add_request(self, service_name, rpc_name, request):
        # TODO: Move rpc/service map to it's own module
        buffered_service = _buffered_rpcs.get(service_name)
        if buffered_service is None:
            return
        buffered_rpc_returns_future = buffered_service.get(rpc_name)
        if buffered_rpc_returns_future is None:
            return
        future_id = _get_next_future_id() if buffered_rpc_returns_future else None
        self._buffer.append(self._BufferEntry(service_name, rpc_name, request, future_id))
        self._active_future_requests = {}
        return _CacheOutcome(
            Empty if future_id is None else EDBObjMessage(id=future_id, is_future=True)
        )

    def flush(self):
        if not self._buffer:
            return
        # TODO: Cleanup stub accessor retrieval
        from ansys.edb.core.session import StubAccessor, StubType

        stub = StubAccessor(StubType.caching).__get__()
        with self._begin_flush():
            request = BufferMessage(buffer=[buffer_entry.msg() for buffer_entry in self._buffer])
            response = stub.FlushBuffer(request)
            cache = get_cache()
            if cache is not None:
                cache.invalidate()
            for updated_edb_obj in response.resolved_futures:
                if (future_edb_obj := self._futures.get(updated_edb_obj.future_id)) is not None:
                    future_edb_obj.msg = updated_edb_obj.edb_obj
                if (
                    future_request := self._active_future_requests.get(updated_edb_obj.future_id)
                ) is not None:
                    future_request.id = updated_edb_obj.edb_obj.id
                    future_request.is_future = (
                        False  # TODO: Will EDBObj have is_future field? May have to use CopyFrom
                    )

    def add_future_ref(self, future):
        self._futures[future.id(False)] = future

    def add_active_future_request(self, future_request):
        self._active_future_requests[future_request.id] = future_request

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


class ServerNotification(Enum):
    """Provides an enum representing the types of server notifications."""

    BEGIN_CACHING = auto()
    END_CACHING = auto()
    INVALIDATE_CACHE = auto()


class IOMangementMode(Enum):
    """Provides an enum representing the types of IO management modes."""

    READ_ONLY = auto()
    WRITE_ONLY = auto()
    READ_AND_WRITE = auto()


def _is_write_operation(service_name, rpc_name):
    # TODO: Need to handle non-buffered write ops
    buffered_service = _buffered_rpcs.get(service_name)
    if buffered_service is None:
        return False
    buffered_rpc_returns_future = buffered_service.get(rpc_name)
    if buffered_rpc_returns_future is None:
        return False
    return True


class _IOManager:
    def __init__(self):
        self._reset()

    def _reset(self):
        self._cache = None
        self._buffer = None
        self._server_notifications = []
        self._active_mode = None

    def start_managing(self, mode):
        self._active_mode = mode
        if (
            self._active_mode == IOMangementMode.READ_ONLY
            or self._active_mode == IOMangementMode.READ_AND_WRITE
        ):
            self._cache = _Cache()
            self.add_notification_for_server(ServerNotification.BEGIN_CACHING)
        if (
            self._active_mode == IOMangementMode.WRITE_ONLY
            or self._active_mode == IOMangementMode.READ_AND_WRITE
        ):
            self._buffer = _Buffer()

    def end_managing(self):
        if (
            self._active_mode == IOMangementMode.READ_ONLY
            or self._active_mode == IOMangementMode.READ_AND_WRITE
        ):
            self.add_notification_for_server(ServerNotification.END_CACHING)
        self._reset()

    @property
    def cache(self):
        """Get the active cache."""
        return self._cache

    @property
    def buffer(self):
        """Get the active buffer."""
        return self._buffer

    @property
    def is_blocking(self):
        """Check if the io manager is currently blocking caching and buffering operations."""
        return (
            self._buffer is not None
            and self._buffer.is_flushing
            or self._cache is not None
            and self._cache.is_refreshing
        )

    def add_notification_for_server(self, notification):
        self._server_notifications.append(notification)

    @property
    def notifications_for_server(self):
        return self._server_notifications

    def clear_notifications_for_server(self):
        self._server_notifications.clear()

    @property
    def is_enabled(self):
        return (self.buffer or self.cache) is not None

    def can_cache(self, service_name, rpc_name):
        return not _is_write_operation(service_name, rpc_name)


MOD.io_manager = _IOManager()


@contextmanager
def enable_io_manager(mode=IOMangementMode.READ_AND_WRITE):
    """Enable caching of data from the server for code called within the context manager and improve performance of \
    read-only operations.

    .. note::
        This is intended for use with read-only operations. If modifications are made to the EDB in this code block, \
        the changes will not be reflected when querying the server until after the context manager is exited.
    """
    try:
        MOD.io_manager.start_managing(mode)
        yield
    finally:
        MOD.io_manager.end_managing()


def get_io_manager():
    """Get the active IO manager."""
    return MOD.io_manager


def get_cache():
    """Get the active cache."""
    return MOD.io_manager.cache if MOD.io_manager is not None else None


def get_buffer():
    """Get the active buffer."""
    return MOD.io_manager.buffer if MOD.io_manager is not None else None
