"""Cache."""
import abc
from collections import defaultdict
from contextlib import contextmanager
from enum import Enum, Flag, auto
from sys import modules

from ansys.api.edb.v1.edb_messages_pb2 import EDBObjCollectionMessage, EDBObjMessage
from ansys.api.edb.v1.io_manager_pb2 import BufferEntryMessage, BufferMessage
from django.utils.module_loading import import_string
from google.protobuf.any_pb2 import Any
from google.protobuf.empty_pb2 import Empty

from ansys.edb.core.inner.rpc_info_utils import get_rpc_info
from ansys.edb.core.inner.utils import client_stream_iterator

# The cache module singleton
MOD = modules[__name__]

_future_id = 0


def _get_next_future_id():
    global _future_id
    _future_id += 1
    return _future_id


def _get_io_manager_stub():
    from ansys.edb.core.session import StubAccessor, StubType

    return StubAccessor(StubType.io_manager).__get__()


class _HijackedOutcome:
    def __init__(self, result):
        self._result = result

    def result(self):
        return self._result


class _IOOptimizer(metaclass=abc.ABCMeta):
    def __init__(self):
        self._is_blocking = False

    @contextmanager
    def block(self):
        try:
            self._is_blocking = True
            yield
        finally:
            self._is_blocking = False
            self._reset_after_block()

    def _reset_after_block(self):
        pass

    @property
    def is_blocking(self):
        return self._is_blocking

    def hijack_request(self, service_name, rpc_name, request):
        hijacked_response = self._hijack_request(service_name, rpc_name, request)
        if hijacked_response is not None:
            return _HijackedOutcome(hijacked_response)
        return None

    @abc.abstractmethod
    def _hijack_request(self, service_name, rpc_name, request):
        pass


class _Cache(_IOOptimizer):
    def __init__(self):
        super().__init__()
        self._response_cache = defaultdict(lambda: defaultdict(lambda: defaultdict()))
        self._msg_type_cache = {}
        self._cached_edb_objs = {}
        self._allow_invalidation = True

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
        self._response_cache[service_name][rpc_method_name][str(request_msg)] = response_msg

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

    def _get_cache_entry(self, service_name, rpc_name, request):
        if (service_cache := self._response_cache.get(service_name)) is not None:
            if (rpc_cache := service_cache.get(rpc_name)) is not None:
                return rpc_cache.get(str(request))

    def _hijack_request(self, service_name, rpc_name, request):
        if (rpc_info := get_rpc_info(service_name, rpc_name)) is None or rpc_info.invalidates_cache:
            if rpc_info is not None and not rpc_info.has_smart_invalidation:
                self.invalidate()
            return
        if rpc_info.has_smart_invalidation and get_invalidation_tracker().is_response_invalidated(
            service_name, rpc_name
        ):
            self.invalidate(service_name, rpc_name, request)
            get_invalidation_tracker().untrack_invalidation(service_name, rpc_name)
        if not rpc_info.can_cache:
            return
        return self._get_cache_entry(service_name, rpc_name, request)

    def invalidate(self, *args):
        if not self._response_cache or not self.allow_invalidation:
            return
        if not args:
            self._response_cache.clear()
            get_invalidation_tracker().clear()
        else:
            if (cache_entry := self._get_cache_entry(*args)) is not None:
                del self._response_cache[args[0]][args[1]][str(args[2])]
        self._cached_edb_objs = self._cached_edb_objs.fromkeys(self._cached_edb_objs, False)
        get_io_manager().add_notification_for_server(ServerNotification.INVALIDATE_CACHE)

    def refresh_for_request(self):
        active_request_edb_obj_msgs = (
            get_io_manager().active_request_edb_obj_msg_mgr.active_request_edb_obj_msgs
        )
        if not active_request_edb_obj_msgs:
            return
        edb_objs_to_refresh = [
            active_request_edb_obj_msg
            for active_request_edb_obj_msg in active_request_edb_obj_msgs.values()
            if not active_request_edb_obj_msg.is_future
            and self._cached_edb_objs.get(active_request_edb_obj_msg.id) is False
        ]
        if not edb_objs_to_refresh:
            return
        with self.block():
            response = _get_io_manager_stub().RefreshCache(
                EDBObjCollectionMessage(items=edb_objs_to_refresh)
            )
            for msg in response.items:
                self.add_from_cache_msg(msg)

    @property
    def allow_invalidation(self):
        return self._allow_invalidation

    @allow_invalidation.setter
    def allow_invalidation(self, allow):
        self._allow_invalidation = allow


class _Buffer(_IOOptimizer):
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
                service_name=self._service_name,
                rpc_name=self._rpc_name,
                request=any_request,
                future_id=self._future_id,
            )
            return msg

    def __init__(self):
        super().__init__()
        self._reset()

    def _reset(self):
        self._buffer = []
        self._futures = defaultdict(list)
        self._invalidate_cache = False
        self._allow_flushing = True

    def _hijack_request(self, service_name, rpc_name, request):
        if (rpc_info := get_rpc_info(service_name, rpc_name)) is None or rpc_info.is_read:
            if (
                rpc_info is None
                or (rpc_info is not None and not rpc_info.has_smart_invalidation)
                or get_invalidation_tracker().is_response_invalidated(service_name, rpc_name)
            ):
                # TODO: Need to clean up invalidation tracker after flushing buffer
                self.flush()
            return
        if not rpc_info.can_buffer:
            return
        if rpc_info.invalidates_cache:
            if rpc_info.has_smart_invalidation:
                get_invalidation_tracker().track_invalidations(service_name, rpc_info.invalidations)
            else:
                self._invalidate_cache = True
        future_id = _get_next_future_id() if rpc_info.returns_future else None
        self._buffer.append(self._BufferEntry(service_name, rpc_name, request, future_id))
        return Empty if future_id is None else EDBObjMessage(id=future_id, is_future=True)

    @staticmethod
    def _buffer_request_iterator(buffer):
        chunk_entry_creator = lambda buffer_entry: buffer_entry.msg()
        chunk_entries_getter = lambda chunk: chunk.buffer
        return client_stream_iterator(
            buffer, BufferMessage, chunk_entry_creator, chunk_entries_getter
        )

    def flush(self):
        if not self._buffer or not self.allow_flushing:
            return
        with self.block():
            if (cache := get_cache()) is not None and self._invalidate_cache:
                cache.invalidate()
            get_io_manager().add_notification_for_server(ServerNotification.FLUSH_BUFFER)
            for response in _get_io_manager_stub().FlushBufferStream(
                self._buffer_request_iterator(self._buffer)
            ):
                for updated_edb_obj in response.resolved_futures:
                    if (
                        future_edb_objs := self._futures.get(updated_edb_obj.future_id)
                    ) is not None:
                        for future_edb_obj in future_edb_objs:
                            future_edb_obj.msg = updated_edb_obj.edb_obj

    def add_future_ref(self, future):
        self._futures[future.id].append(future)

    def _reset_after_block(self):
        self._reset()

    @property
    def allow_flushing(self):
        return self._allow_flushing

    @allow_flushing.setter
    def allow_flushing(self, allow):
        self._allow_flushing = allow


class ServerNotification(Enum):
    """Provides an enum representing the types of server notifications."""

    INVALIDATE_CACHE = auto()
    FLUSH_BUFFER = auto()
    RESET_FUTURE_TRACKING = auto()


class IOMangementType(Flag):
    """Provides an enum representing the types of IO management modes."""

    READ = auto()
    WRITE = auto()
    READ_AND_WRITE = READ | WRITE
    NO_CACHE_INVALIDATION = auto()
    NO_BUFFER_FLUSHING = auto()
    NO_CACHE_INVALIDATION_NO_BUFFER_FLUSHING = NO_CACHE_INVALIDATION | NO_BUFFER_FLUSHING


class _ActiveRequestEdbObjMsgMgr:
    def __init__(self):
        self._active_request_edb_obj_msgs = {}

    @staticmethod
    def _get_key(msg_id, is_future):
        return f"{msg_id}-{is_future}"

    def add_active_request_edb_obj_msg(self, msg):
        self._active_request_edb_obj_msgs[self._get_key(msg.id, msg.is_future)] = msg

    def resolve_future(self, future_id, resolved_id):
        key = self._get_key(future_id, True)
        if key in self._active_request_edb_obj_msgs:
            msg = self._active_request_edb_obj_msgs.pop(key)
            msg.id = resolved_id
            msg.is_future = False
            self.add_active_request_edb_obj_msg(msg)

    def reset(self):
        self._active_request_edb_obj_msgs.clear()

    @property
    def active_request_edb_obj_msgs(self):
        return self._active_request_edb_obj_msgs


class _InvalidationTracker:
    def __init__(self):
        self._invalidation_tracker = defaultdict(lambda: defaultdict(set))
        self._active_obj = None
        self._class_invalidation_tracker = defaultdict(set)

    def track_active_obj(self, active_obj):
        self._active_obj = active_obj

    def untrack_active_obj(self):
        self._active_obj = None

    def track_invalidations(self, service_name, invalidations):
        is_active_rpc_class_level = isinstance(self._active_obj, type)
        obj_invalidations = (
            None if is_active_rpc_class_level else self._invalidation_tracker[self._active_obj.id]
        )
        for invalidation in invalidations:
            invalidated_service_name = (
                service_name if invalidation.is_self_invalidation else invalidation.service
            )
            invalidations = (
                obj_invalidations
                if invalidation.is_self_invalidation
                else self._class_invalidation_tracker
            )
            invalidations[invalidated_service_name].add(invalidation.rpc)
            # TODO: Need to handle class level invalidations specified by class level invalidations
            # TODO: Handle invalidations made by derived class

    def untrack_invalidation(self, service_name, rpc):
        is_class_level = isinstance(self._active_obj, type)
        if not is_class_level:
            self._invalidation_tracker[self._active_obj.id][service_name].remove(rpc)
        else:
            self._class_invalidation_tracker[service_name].remove(rpc)

    def is_response_invalidated(self, service_name, rpc_name):
        is_class_level = isinstance(self._active_obj, type)
        invalidations = (
            self._class_invalidation_tracker
            if is_class_level
            else self._invalidation_tracker.get(self._active_obj.id)
        )
        if invalidations is not None:
            if (service_invalidations := invalidations.get(service_name)) is not None:
                return rpc_name in service_invalidations
        return False

    def clear(self):
        self._invalidation_tracker.clear()


class _IOManager:
    def __init__(self):
        self._reset()
        self._server_notifications = set()

    def _reset(self):
        self._cache = None
        self._buffer = None
        self._active_request_edb_obj_msg_mgr = _ActiveRequestEdbObjMsgMgr()

    @staticmethod
    def _enable_caching(enable):
        from ansys.edb.core.inner.messages import bool_message

        _get_io_manager_stub().EnableCache(bool_message(enable))

    def start_managing(self, mode):
        if IOMangementType.READ in mode:
            self._cache = _Cache()
            self._enable_caching(True)
        if IOMangementType.WRITE in mode:
            self._buffer = _Buffer()
        if IOMangementType.NO_CACHE_INVALIDATION in mode:
            self._cache.allow_invalidation = False
        if IOMangementType.NO_BUFFER_FLUSHING in mode:
            self._buffer.allow_flushing = False
        self._invalidation_tracker = _InvalidationTracker()

    def end_managing(self):
        if self._cache is not None:
            self._enable_caching(False)
        if self._buffer is not None:
            self._buffer.allow_flushing = True
            self._buffer.flush()
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
    def invalidation_tracker(self):
        """Get the invalidation tracker."""
        return self._invalidation_tracker

    @property
    def is_blocking(self):
        """Check if the io manager is currently blocking caching and buffering operations."""
        return (
            self.cache is not None
            and self.cache.is_blocking
            or self.buffer is not None
            and self.buffer.is_blocking
        )

    def add_notification_for_server(self, notification):
        self._server_notifications.add(notification)

    def get_notifications_for_server(self, pop=False):
        if not pop:
            return self._server_notifications
        server_notifications = self._server_notifications
        self._server_notifications = set()
        return server_notifications

    @property
    def is_enabled(self):
        return (self.buffer or self.cache) is not None

    @property
    def active_request_edb_obj_msg_mgr(self):
        return self._active_request_edb_obj_msg_mgr

    @contextmanager
    def manage_io(self):
        try:
            yield
        finally:
            self.active_request_edb_obj_msg_mgr.reset()


MOD.io_manager = _IOManager()


@contextmanager
def enable_io_manager(io_type=IOMangementType.READ_AND_WRITE):
    """Enable caching of data from the server for code called within the context manager and improve performance of \
    read-only operations.

    .. note::
        This is intended for use with read-only operations. If modifications are made to the EDB in this code block, \
        the changes will not be reflected when querying the server until after the context manager is exited.
    """
    try:
        MOD.io_manager.start_managing(io_type)
        yield
    finally:
        MOD.io_manager.end_managing()


def get_io_manager():
    """Get the active IO manager."""
    return MOD.io_manager


def get_cache():
    """Get the active cache."""
    return MOD.io_manager.cache


def get_buffer():
    """Get the active buffer."""
    return MOD.io_manager.buffer


def get_invalidation_tracker():
    """Get the active buffer."""
    return MOD.io_manager.invalidation_tracker


def start_managing(io_type):
    """Begin managing IO operations of the specified type.

    Parameters
    ----------
    io_type : IOMangementMode

    """
    MOD.io_manager.start_managing(io_type)


def end_managing():
    """End management of IO operations."""
    MOD.io_manager.end_managing()
