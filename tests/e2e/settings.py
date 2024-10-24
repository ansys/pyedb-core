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

import os
import tempfile

# configs are initialized with system environment variables. Can be manually overwritten.
configs = {**os.environ}


def server_exe_dir():
    """ANSYS EM Root directory where EDB_RPC_Server.exe is located."""
    if "ANSYSEM_EDB_EXE_DIR" in configs:
        return configs["ANSYSEM_EDB_EXE_DIR"]
    # TODO: add 'VERSION=23.2/24.1/etc' and look for system installation


def temp_dir():
    """Temporary directory. system default if unspecified."""
    if "ANSYSEM_EDB_TEMP_DIR" in configs:
        return configs["ANSYSEM_EDB_TEMP_DIR"]
    return tempfile.mkdtemp()
