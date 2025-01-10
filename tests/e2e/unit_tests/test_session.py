from contextlib import closing
from pathlib import Path
import socket

import settings

from ansys.edb.core.database import Database
from ansys.edb.core.session import _Session, launch_session


def test_default_port_in_use(tmp_path: Path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 50051))
        sess: _Session = launch_session(settings.server_exe_dir())
        try:
            edb_path = tmp_path / "p1.aedb"
            with closing(Database.create(edb_path.as_posix())) as db:
                assert not db.is_null
        finally:
            sess.disconnect()
