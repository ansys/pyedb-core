"""Scratch tests for the rpc_executor C++ extension module.

Run with::

    pytest tests/e2e/scratch/test_rpc_executor.py -v

Tests that exercise the real EDB_RPC_Services library require the
``ANSYSEM_EDB_EXE_DIR`` environment variable to point to an Ansys EM install
directory containing ``EDB_RPC_Services.dll`` (Windows) or
``libEDB_RPC_Services.so`` (Linux).  Those tests are skipped automatically
when the variable is unset.

Tests that verify failure-mode behaviour (bad path, pre-initialize call) run
unconditionally and do not need a real EDB install.
"""

import os

import pytest
import rpc_executor

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

EDB_EXE_DIR = os.environ.get("ANSYSEM_EDB_EXE_DIR")

requires_install = pytest.mark.skipif(
    not EDB_EXE_DIR,
    reason="ANSYSEM_EDB_EXE_DIR not set — skipping tests that require a real EDB install",
)

# ---------------------------------------------------------------------------
# Tests that do NOT need a real EDB install
# ---------------------------------------------------------------------------


def test_module_exposes_expected_callables():
    """The compiled extension must expose initialize() and execute_rpc()."""
    assert callable(rpc_executor.initialize)
    assert callable(rpc_executor.execute_rpc)


def test_initialize_with_nonexistent_path_returns_false():
    """initialize() must return False for a path that does not exist."""
    result = rpc_executor.initialize("/does/not/exist/at/all")
    assert result is False, "Expected False for a non-existent directory"


def test_initialize_with_empty_string_returns_false():
    """initialize() must return False for an empty path."""
    result = rpc_executor.initialize("")
    assert result is False, "Expected False for an empty directory path"


def test_execute_rpc_before_initialize_raises_runtime_error():
    """execute_rpc() must raise RuntimeError when Initialize() was never called.

    This test is only meaningful when run in isolation before any successful
    initialize() call.  When ANSYSEM_EDB_EXE_DIR is set, the @requires_install
    tests that run before this one will have already called initialize(), so
    g_plugin will be non-null and this test is skipped automatically.
    """
    if EDB_EXE_DIR:
        pytest.skip(
            "ANSYSEM_EDB_EXE_DIR is set; initialize() will have already been "
            "called by an earlier test — g_plugin is non-null.  Run this test "
            "file in isolation (without ANSYSEM_EDB_EXE_DIR) to exercise the "
            "uninitialized guard."
        )
    with pytest.raises(RuntimeError, match="not initialized"):
        rpc_executor.execute_rpc("SomeService", "SomeMethod", b"")


# ---------------------------------------------------------------------------
# Tests that require a real EDB install
# ---------------------------------------------------------------------------


@requires_install
def test_initialize_with_valid_dir_returns_true():
    """initialize() must return True for a valid Ansys EM install directory."""
    ok = rpc_executor.initialize(EDB_EXE_DIR)
    assert ok, f"rpc_executor.initialize({EDB_EXE_DIR!r}) returned False"


@requires_install
def test_initialize_is_noop_after_first_success():
    """After the first successful initialize(), further calls are a no-op.

    The second call uses a deliberately wrong path; if Initialize() re-ran it
    would return False.  It must return True because g_plugin is already set.
    """
    rpc_executor.initialize(EDB_EXE_DIR)
    ok = rpc_executor.initialize("/does/not/exist")
    assert ok, "Second call to initialize() should be a no-op and return True"


@requires_install
def test_execute_rpc_returns_three_tuple():
    """execute_rpc() must return a (bool, bytes, str) 3-tuple."""
    rpc_executor.initialize(EDB_EXE_DIR)
    result = rpc_executor.execute_rpc("EDBServer", "GetVersion", b"")
    assert isinstance(result, tuple), "execute_rpc() did not return a tuple"
    assert len(result) == 3, f"Expected 3-tuple, got length {len(result)}"
    ok, response, error = result
    assert isinstance(ok, bool), f"result[0] should be bool, got {type(ok)}"
    assert isinstance(response, bytes), f"result[1] should be bytes, got {type(response)}"
    assert isinstance(error, str), f"result[2] should be str, got {type(error)}"


@requires_install
def test_execute_rpc_serialized_request_must_be_bytes():
    """execute_rpc() must reject a non-bytes serialized_request argument."""
    rpc_executor.initialize(EDB_EXE_DIR)
    with pytest.raises(TypeError):
        rpc_executor.execute_rpc("EDBServer", "GetVersion", "not-bytes")
