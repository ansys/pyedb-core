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

"""This package defines exception base classes."""

from enum import Enum


class ErrorCode(Enum):
    """Provides EDB exception types."""

    UNKNOWN = "Unknown exception: {}."
    UNAVAILABLE = (
        "EDB server is not accessible. Make sure an instance is listening on the specified port.."
    )
    NO_SESSIONS = "No active session is detected."
    STARTUP_UNEXPECTED = "An unexpected error occurred when starting the local server: {}."
    STARTUP_TIMEOUT = "Could not start local server: Time out"
    STARTUP_MULTI_SESSIONS = "There can be only one session active at a time."
    STARTUP_NO_EXECUTABLE = (
        "Could not find necessary executables. Make sure the Ansys EM root directory is correct."
    )
    STARTUP_FAILURE_LICENSE = "Could not start the local server: No valid license detected."
    STARTUP_FAILURE_EDB = "Could not start the local server: Failed to initialize EDB."
    STARTUP_FAILURE = "Could not start the local server due to unknown reason."

    INVALID_ARGUMENT = "{}"


def _message(code, *args):
    template = code.value
    return template.format(*args)


class EDBSessionException(Exception):
    """Provides the base class for exceptions related to EDB sessions."""

    def __init__(self, code, *args):
        """Initialize EDBSessionException."""
        super().__init__(_message(code, *args))
        self._code = code


class InvalidArgumentException(EDBSessionException):
    """Provides the exception that occurs when a request fails due to an invalid argument."""

    def __init__(self, response):
        """Initialize InvalidArgumentException."""
        super().__init__(ErrorCode.INVALID_ARGUMENT, response.details())
        self._response = response
