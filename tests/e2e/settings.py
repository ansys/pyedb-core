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
