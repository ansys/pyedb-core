# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Client-side gRPC interceptors."""

import abc
import logging

from grpc import StatusCode, UnaryUnaryClientInterceptor

from ansys.edb.core.inner.exceptions import EDBSessionException, ErrorCode, InvalidArgumentException


class Interceptor(UnaryUnaryClientInterceptor, metaclass=abc.ABCMeta):
    """Provides the base interceptor class."""

    def __init__(self, logger):
        """Initialize a base interceptor with a logger."""
        super().__init__()
        self._logger = logger

    @abc.abstractmethod
    def _post_process(self, response):
        pass

    def intercept_unary_unary(self, continuation, client_call_details, request):
        """Intercept a gRPC call."""
        response = continuation(client_call_details, request)

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
