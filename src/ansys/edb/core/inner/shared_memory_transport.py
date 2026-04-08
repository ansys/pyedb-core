"""Shared-memory IPC transport for pyedb-core.

Provides :class:`SharedMemoryTransport`, a low-level wrapper around a
shared-memory region created by EDB_RPC_Server, and
:class:`SharedMemoryInterceptor`, a gRPC client interceptor that routes
all RPC calls through the shared-memory channel instead of the network.
"""

from __future__ import annotations

from multiprocessing import shared_memory
import os
import struct
import subprocess
import time

# ---------------------------------------------------------------------------
# Constants — must match SharedMemoryRPCManager.h
# ---------------------------------------------------------------------------

SHM_HEADER_SIZE = 64
SHM_SERVICE_NAME_SIZE = 256
SHM_RPC_NAME_SIZE = 256
SHM_DATA_OFFSET = SHM_HEADER_SIZE + SHM_SERVICE_NAME_SIZE + SHM_RPC_NAME_SIZE

# Header field offsets
OFF_STATE = 0
OFF_REQUEST_SIZE = 4
OFF_RESPONSE_SIZE = 8
OFF_ERROR_SIZE = 12
OFF_SUCCESS = 16

# State machine values
STATE_IDLE = 0
STATE_REQUEST_READY = 1
STATE_RESPONSE_READY = 2
STATE_ERROR = 3
STATE_SHUTDOWN = 4

# Default shared memory size: 50 MB (must match server default).
SHM_DEFAULT_SIZE_MB = 50
SHM_BYTES_PER_MB = 1024 * 1024

# Spin-wait tuning: number of tight spin iterations before yielding.
_SPIN_ITERATIONS = 10000

# How often (in seconds of wall-clock time) to check if the server is alive
# during the spin-wait loop.  Kept high enough to avoid polling overhead.
_SERVER_ALIVE_CHECK_INTERVAL = 1.0


# ---------------------------------------------------------------------------
# SharedMemoryTransport
# ---------------------------------------------------------------------------


class SharedMemoryTransport:
    """Low-level transport over a shared-memory block created by EDB_RPC_Server.

    The server must already be running in shared-memory mode and the
    shared-memory region must exist.  Synchronization is purely via
    spin-wait on the shared-memory state field — no kernel objects are used.

    Parameters
    ----------
    shm_name : str
        Name of the shared-memory region (matches ``-shm`` CLI arg on server).
    shm_size_mb : int, optional
        Size of the shared memory region in MB. 0 means use the environment
        variable ``ANSYS_EDB_SHM_SIZE_MB`` or the default (50 MB).
    """

    def __init__(
        self,
        shm_name: str,
        shm_size_mb: int = 0,
        server_process: subprocess.Popen | None = None,
    ):
        """Create the transport object."""
        self._shm_name = shm_name
        self._shm_size = self._resolve_size(shm_size_mb)
        self._shm: shared_memory.SharedMemory | None = None
        self._buf: memoryview | None = None
        self._server_process = server_process

    @staticmethod
    def _resolve_size(requested_mb: int) -> int:
        mb = requested_mb
        if mb <= 0:
            env_val = os.environ.get("ANSYS_EDB_SHM_SIZE_MB")
            if env_val:
                try:
                    mb = int(env_val)
                except ValueError:
                    mb = 0
        if mb <= 0:
            mb = SHM_DEFAULT_SIZE_MB
        return mb * SHM_BYTES_PER_MB

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def connect(self):
        """Attach to the shared memory block."""
        self._shm = shared_memory.SharedMemory(
            name=self._shm_name, create=False, size=self._shm_size
        )
        self._buf = self._shm.buf

    def disconnect(self):
        """Detach from the shared memory (does NOT unlink — server owns cleanup)."""
        if self._shm:
            self._shm.close()
            self._shm = None
            self._buf = None

    def shutdown(self):
        """Signal the server to shut down via the shared memory state."""
        self._write_state(STATE_SHUTDOWN)

    # ------------------------------------------------------------------
    # RPC execution
    # ------------------------------------------------------------------

    def execute_rpc(
        self, service_name: str, rpc_name: str, serialized_request: bytes
    ) -> tuple[bool, bytes, str]:
        """Send a serialized RPC request and wait for the response.

        Returns
        -------
        tuple[bool, bytes, str]
            (success, serialized_response, error_message)
        """
        buf = self._buf
        assert buf is not None, "SharedMemoryTransport not connected"

        max_data_size = self._shm_size - SHM_DATA_OFFSET

        if len(serialized_request) > max_data_size:
            return (
                False,
                b"",
                f"Request size ({len(serialized_request)} bytes) exceeds "
                f"shared memory capacity ({max_data_size} bytes)",
            )

        # Write service name (null-terminated)
        svc_bytes = service_name.encode("utf-8")[: SHM_SERVICE_NAME_SIZE - 1]
        buf[SHM_HEADER_SIZE : SHM_HEADER_SIZE + len(svc_bytes)] = svc_bytes
        buf[SHM_HEADER_SIZE + len(svc_bytes)] = 0

        # Write RPC name (null-terminated)
        rpc_offset = SHM_HEADER_SIZE + SHM_SERVICE_NAME_SIZE
        rpc_bytes = rpc_name.encode("utf-8")[: SHM_RPC_NAME_SIZE - 1]
        buf[rpc_offset : rpc_offset + len(rpc_bytes)] = rpc_bytes
        buf[rpc_offset + len(rpc_bytes)] = 0

        # Write request size and data
        req_size = len(serialized_request)
        self._write_u32(OFF_REQUEST_SIZE, req_size)
        buf[SHM_DATA_OFFSET : SHM_DATA_OFFSET + req_size] = serialized_request

        # Transition state to REQUEST_READY — the server spin-waits on this.
        self._write_state(STATE_REQUEST_READY)

        # Spin-wait for the server to write RESPONSE_READY.
        self._spin_wait_for_response()

        # Read the response
        success = self._read_u32(OFF_SUCCESS) != 0
        resp_size = self._read_u32(OFF_RESPONSE_SIZE)
        err_size = self._read_u32(OFF_ERROR_SIZE)

        if success:
            serialized_response = bytes(buf[SHM_DATA_OFFSET : SHM_DATA_OFFSET + resp_size])
            return (True, serialized_response, "")
        else:
            error_message = bytes(buf[SHM_DATA_OFFSET : SHM_DATA_OFFSET + err_size]).decode(
                "utf-8", errors="replace"
            )
            return (False, b"", error_message)

    # ------------------------------------------------------------------
    # Spin-wait
    # ------------------------------------------------------------------

    def _spin_wait_for_response(self):
        """Spin-read the state field until RESPONSE_READY (or ERROR/SHUTDOWN).

        Periodically checks whether the server process is still alive so that
        a server crash surfaces as a clear exception instead of an infinite hang.
        """
        buf = self._buf
        assert buf is not None
        last_alive_check = time.monotonic()
        while True:
            # Phase 1: tight spin
            for _ in range(_SPIN_ITERATIONS):
                state = struct.unpack_from("<I", buf, OFF_STATE)[0]
                if state == STATE_RESPONSE_READY or state == STATE_ERROR:
                    return
                if state == STATE_SHUTDOWN:
                    raise RuntimeError("Server shut down unexpectedly")
            # Phase 2: yield to OS to avoid burning a full core when idle
            time.sleep(0)
            # Phase 3: periodically verify the server process is still running
            now = time.monotonic()
            if now - last_alive_check >= _SERVER_ALIVE_CHECK_INTERVAL:
                last_alive_check = now
                self._check_server_alive()

    # ------------------------------------------------------------------
    # Low-level helpers
    # ------------------------------------------------------------------

    def _check_server_alive(self):
        """Raise if the server process has exited."""
        proc = self._server_process
        if proc is None:
            return
        if proc.poll() is not None:
            rc = proc.returncode
            raise RuntimeError(
                f"EDB_RPC_Server process exited unexpectedly "
                f"(exit code {rc}) while waiting for an RPC response"
            )

    def _read_u32(self, offset: int) -> int:
        assert self._buf is not None
        return struct.unpack_from("<I", self._buf, offset)[0]

    def _write_u32(self, offset: int, value: int):
        assert self._buf is not None
        struct.pack_into("<I", self._buf, offset, value)

    def _write_state(self, state: int):
        """Write the state field with a release-style write.

        All preceding writes to the buffer (request data, sizes, names) must
        be visible to the other process before the state transition.  On x86
        this is guaranteed by the strong memory model (stores are not
        reordered w.r.t. other stores), so a plain write suffices.
        """
        assert self._buf is not None
        struct.pack_into("<I", self._buf, OFF_STATE, state)
