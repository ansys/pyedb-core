"""Client-side gRPC interceptors."""

import abc
from collections import namedtuple
import logging

from grpc import (
    ClientCallDetails,
    StatusCode,
    StreamStreamClientInterceptor,
    UnaryStreamClientInterceptor,
    UnaryUnaryClientInterceptor,
)

from ansys.edb.core.inner.exceptions import EDBSessionException, ErrorCode, InvalidArgumentException
from ansys.edb.core.inner.rpc_info_utils import can_cache
from ansys.edb.core.utility.io_manager import ServerNotification, get_io_manager


class Interceptor(
    UnaryUnaryClientInterceptor,
    UnaryStreamClientInterceptor,
    StreamStreamClientInterceptor,
    metaclass=abc.ABCMeta,
):
    """Provides the base interceptor class."""

    def __init__(self, logger):
        """Initialize a base interceptor with a logger."""
        super().__init__()
        self._logger = logger

    @abc.abstractmethod
    def _post_process(self, response):
        pass

    def _continue_unary_unary(self, continuation, client_call_details, request):
        return continuation(client_call_details, request)

    def intercept_unary_unary(self, continuation, client_call_details, request):
        """Intercept a gRPC call."""
        response = self._continue_unary_unary(continuation, client_call_details, request)

        self._post_process(response)

        return response

    def intercept_unary_stream(self, continuation, client_call_details, request):
        """Intercept a gRPC streaming call."""
        return continuation(client_call_details, request)

    def intercept_stream_stream(self, continuation, client_call_details, request_iterator):
        """Intercept a gRPC streaming call."""
        return continuation(client_call_details, request_iterator)


class LoggingInterceptor(Interceptor):
    """Logs EDB errors on each request."""

    _LOG_LEVELS = {
        "log-fatal": logging.CRITICAL,
        "log-error": logging.ERROR,
        "log-warn": logging.WARN,
        "log-info": logging.INFO,
    }

    def _handler(self, log_level):
        if log_level == logging.CRITICAL:
            return self._logger.critical
        elif log_level == logging.WARN:
            return self._logger.warning
        elif log_level == logging.ERROR:
            return self._logger.error
        elif log_level == logging.INFO:
            return self._logger.info
        else:
            return self._logger.logger

    def _post_process(self, response):
        tm = response.trailing_metadata()
        if tm is not None:
            for kv in tm:
                if kv[0] in self._LOG_LEVELS:
                    handler = self._handler(self._LOG_LEVELS[kv[0]])
                    handler(kv[1])


class ExceptionInterceptor(Interceptor):
    """Handles general gRPC errors on each request."""

    def _post_process(self, response):
        code = response.code()
        exception = None

        if code == StatusCode.UNAVAILABLE:
            exception = EDBSessionException(ErrorCode.UNAVAILABLE)
            self._logger.critical(repr(exception))
        elif code == StatusCode.INVALID_ARGUMENT:
            exception = InvalidArgumentException(response)
            self._logger.error(repr(exception))

        if exception is not None:
            raise exception


class IOInterceptor(Interceptor):
    """Returns cached values if a given request has already been made and caching is enabled."""

    def __init__(self, logger, rpc_counter):
        """Initialize a caching interceptor with a logger and rpc counter."""
        super().__init__(logger)
        self._rpc_counter = rpc_counter
        self._reset_cache_entry_data()

    def _reset_cache_entry_data(self):
        self._current_rpc_method = ""
        self._current_cache_key_details = None
        self._hijacked = False

    def _should_log_traffic(self):
        return self._rpc_counter is not None

    class _ClientCallDetails(
        namedtuple("_ClientCallDetails", ("method", "timeout", "metadata", "credentials")),
        ClientCallDetails,
    ):
        pass

    @staticmethod
    def _add_caching_option_to_metadata(metadata, option, is_enabled):
        metadata.append((option, "1" if is_enabled else "0"))

    @classmethod
    def _get_client_call_details_with_caching_options(cls, client_call_details):
        io_mgr = get_io_manager()
        if not io_mgr.get_notifications_for_server():
            return client_call_details
        metadata = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        for notification in io_mgr.get_notifications_for_server(True):
            if notification == ServerNotification.INVALIDATE_CACHE:
                cls._add_caching_option_to_metadata(metadata, "invalidate-cache", True)
            elif notification == ServerNotification.FLUSH_BUFFER:
                cls._add_caching_option_to_metadata(metadata, "flush-buffer", True)
            elif notification == ServerNotification.RESET_FUTURE_TRACKING:
                cls._add_caching_option_to_metadata(metadata, "reset-future-tracking", True)
        return cls._ClientCallDetails(
            client_call_details.method,
            client_call_details.timeout,
            metadata,
            client_call_details.credentials,
        )

    @staticmethod
    def _attempt_hijack(*args):
        io_manager = get_io_manager()
        hijacked_response = None
        if (buffer := io_manager.buffer) is not None:
            hijacked_response = buffer.hijack_request(*args)
        if hijacked_response is None and (cache := io_manager.cache) is not None:
            hijacked_response = cache.hijack_request(*args)
        return hijacked_response

    def _hijack(self, client_call_details, request):
        io_manager = get_io_manager()
        if io_manager.is_enabled and not io_manager.is_blocking:
            with io_manager.manage_io():
                method_tokens = client_call_details.method.strip("/").split("/")
                cache_key_details = method_tokens[0], method_tokens[1], request
                if (hijacked_result := self._attempt_hijack(*cache_key_details)) is not None:
                    self._hijacked = True
                    return hijacked_result
                if io_manager.cache is not None and can_cache(
                    cache_key_details[0], cache_key_details[1]
                ):
                    self._current_cache_key_details = cache_key_details
                io_manager.add_notification_for_server(ServerNotification.RESET_FUTURE_TRACKING)
        if self._should_log_traffic():
            self._current_rpc_method = client_call_details.method

    def _continue_unary_unary(self, continuation, client_call_details, request):
        if (hijacked_result := self._hijack(client_call_details, request)) is not None:
            return hijacked_result
        return super()._continue_unary_unary(
            continuation,
            self._get_client_call_details_with_caching_options(client_call_details),
            request,
        )

    def _post_process(self, response):
        io_manager = get_io_manager()
        if (cache := io_manager.cache) is not None and self._current_cache_key_details is not None:
            cache.add(*self._current_cache_key_details, response.result())
        if self._should_log_traffic() and not self._hijacked:
            self._rpc_counter[self._current_rpc_method] += 1
        self._reset_cache_entry_data()

    def intercept_unary_stream(self, continuation, client_call_details, request):
        """Intercept a gRPC streaming call."""
        if (hijacked_result := self._hijack(client_call_details, request)) is not None:
            return hijacked_result
        return super().intercept_unary_stream(
            continuation,
            self._get_client_call_details_with_caching_options(client_call_details),
            request,
        )

    def intercept_stream_stream(self, continuation, client_call_details, request_iterator):
        """Intercept a gRPC streaming call."""
        if (hijacked_result := self._hijack(client_call_details, request_iterator)) is not None:
            return hijacked_result
        return super().intercept_stream_stream(
            continuation,
            self._get_client_call_details_with_caching_options(client_call_details),
            request_iterator,
        )
