"""Client-side gRPC interceptors."""

import abc
from collections import namedtuple
import logging

from grpc import (
    ClientCallDetails,
    StatusCode,
    UnaryStreamClientInterceptor,
    UnaryUnaryClientInterceptor,
)

from ansys.edb.core.inner.exceptions import EDBSessionException, ErrorCode, InvalidArgumentException
from ansys.edb.core.utility.io_manager import get_io_manager


class Interceptor(UnaryUnaryClientInterceptor, UnaryStreamClientInterceptor, metaclass=abc.ABCMeta):
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


class CachingInterceptor(Interceptor):
    """Returns cached values if a given request has already been made and caching is enabled."""

    def __init__(self, logger, rpc_counter):
        """Initialize a caching interceptor with a logger and rpc counter."""
        super().__init__(logger)
        self._rpc_counter = rpc_counter
        self._reset_cache_entry_data()

    def _reset_cache_entry_data(self):
        self._current_rpc_method = ""
        self._current_cache_key_details = None

    def _should_log_traffic(self):
        return self._rpc_counter is not None

    class _ClientCallDetails(
        namedtuple("_ClientCallDetails", ("method", "timeout", "metadata", "credentials")),
        ClientCallDetails,
    ):
        pass

    @classmethod
    def _get_client_call_details_with_caching_options(cls, client_call_details):
        if get_io_manager() is None:
            return client_call_details
        metadata = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        metadata.append(("enable-caching", "1"))
        return cls._ClientCallDetails(
            client_call_details.method,
            client_call_details.timeout,
            metadata,
            client_call_details.credentials,
        )

    def _continue_unary_unary(self, continuation, client_call_details, request):
        if self._should_log_traffic():
            self._current_rpc_method = client_call_details.method
        if (io_manager := get_io_manager()) is not None and not io_manager.buffer.is_flushing:
            method_tokens = client_call_details.method.strip("/").split("/")
            cache_key_details = method_tokens[0], method_tokens[1], request
            buffer_result = io_manager.buffer.add_request(*cache_key_details)
            if buffer_result is not None:
                return buffer_result
            io_manager.buffer.flush()
            cached_response = io_manager.cache.get(*cache_key_details)
            if cached_response is not None:
                return cached_response
            else:
                self._current_cache_key_details = cache_key_details
        return super()._continue_unary_unary(
            continuation,
            self._get_client_call_details_with_caching_options(client_call_details),
            request,
        )

    def _cache_missed(self):
        return self._current_cache_key_details is not None

    def _post_process(self, response):
        io_manager = get_io_manager()
        if io_manager is not None and self._cache_missed() and not io_manager.buffer.is_flushing:
            io_manager.cache.add(*self._current_cache_key_details, response.result())
        if self._should_log_traffic() and (io_manager is None or self._cache_missed()):
            self._rpc_counter[self._current_rpc_method] += 1
        self._reset_cache_entry_data()

    def intercept_unary_stream(self, continuation, client_call_details, request):
        """Intercept a gRPC streaming call."""
        return super().intercept_unary_stream(
            continuation,
            self._get_client_call_details_with_caching_options(client_call_details),
            request,
        )
