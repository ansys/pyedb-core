"""Cache."""

from contextlib import contextmanager
from sys import modules

from django.utils.module_loading import import_string

# The cache module singleton
MOD = modules[__name__]
MOD.cache = None


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

    class _CacheOutcome:
        def __init__(self, result):
            self._result = result

        def result(self):
            return self._result

    def add(self, service_name, rpc_method_name, request_msg, response_msg):
        key = self._generate_cache_key(service_name, rpc_method_name, request_msg)
        self._response_cache[key] = self._CacheOutcome(response_msg)

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


@contextmanager
def enable_caching():
    """Enable caching of data from the server for code called within the context manager and improve performance of \
    read-only operations.

    .. note::
        This is intended for use with read-only operations. If modifications are made to the EDB in this code block, \
        the changes will not be reflected when querying the server until after the context manager is exited.
    """
    try:
        MOD.cache = _Cache()
        yield
    finally:
        MOD.cache = None


def get_cache():
    """Get the active cache."""
    return MOD.cache
