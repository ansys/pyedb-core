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
