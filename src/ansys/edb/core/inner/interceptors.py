"""Client-side gRPC interceptors."""

import abc
import hashlib
import logging

from grpc import StatusCode, UnaryUnaryClientInterceptor

from ansys.edb.core.inner.exceptions import EDBSessionException, ErrorCode, InvalidArgumentException


class Interceptor(UnaryUnaryClientInterceptor, metaclass=abc.ABCMeta):
    """Provides the base interceptor class."""

    def __init__(self, logger):
        """Initialize a base interceptor with a logger."""
        super().__init__()
        self._logger = logger
        self._cache = {}

    @abc.abstractmethod
    def _post_process(self, response):
        pass

    def _generate_cache_key(self, client_call_details, request):
        """Generate a unique cache key based on the request."""
        key = f"{client_call_details.method}-{str(request)}"
        return hashlib.md5(key.encode()).hexdigest()

    def intercept_unary_unary(self, continuation, client_call_details, request):
        """Intercept a gRPC call."""
        cache_key = self._generate_cache_key(client_call_details, request)
        cached_response = self._cache.get(cache_key)
        if cached_response is not None:
            return cached_response

        response = continuation(client_call_details, request)
        self._cache[cache_key] = response

        self._post_process(response)

        return response


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
