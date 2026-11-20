# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

from contextlib import closing
from pathlib import Path
import socket

import settings

from ansys.edb.core.database import Database
import ansys.edb.core.session as session


def test_launch_session_when_default_port_in_use(new_database_path: Path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 50051))
        sess: session._Session = session.launch_session(settings.server_exe_dir())
        try:
            assert isinstance(sess.port_num, int) and sess.port_num != 50051
            with closing(Database.create(new_database_path)) as db:
                assert not db.is_null
        finally:
            sess.disconnect()


def test_session_when_default_port_in_use(new_database_path: Path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 50051))
        with session.session(settings.server_exe_dir()):
            sess: session._Session = session.MOD.current_session
            assert isinstance(sess.port_num, int) and sess.port_num != 50051
            with closing(Database.create(new_database_path)) as db:
                assert not db.is_null
