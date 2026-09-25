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

"""Root conftest for e2e tests.

Provides session-scoped server fixture, asset path resolution,
and helper fixtures for temporary EDB copies.
"""

import os
from pathlib import Path
import re
import shutil

import pytest

from ansys.edb.core.database import Database
from ansys.edb.core.layout.cell import Cell
from ansys.edb.core.layout.cell import CellType
from ansys.edb.core.session import session


def _resolve_ansysem_install() -> str:
    """Return the AnsysEM install directory from environment variables."""
    explicit = os.environ.get("ANSYS_EDB_CORE_INSTALL_DIR", "")
    if explicit:
        return explicit
    best_version, best_dir = -1, ""
    for key, value in os.environ.items():
        m = re.fullmatch(r"ANSYSEM_ROOT(\d+)", key)
        if m and int(m.group(1)) > best_version:
            best_version, best_dir = int(m.group(1)), value
    return best_dir


def _server_available() -> bool:
    """Check whether the EDB server can be launched."""
    install_dir = _resolve_ansysem_install()
    if not install_dir:
        return False
    return Path(install_dir).is_dir()


# ---------------------------------------------------------------------------
# Marks registration
# ---------------------------------------------------------------------------


def pytest_addoption(parser):
    parser.addoption(
        "--use-shared-memory",
        action="store_true",
        default=True,
        help="Use shared-memory IPC for client/server communication (default: enabled).",
    )
    parser.addoption(
        "--no-shared-memory",
        action="store_true",
        default=False,
        help="Disable shared-memory IPC and use standard gRPC communication.",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "requires_server: test requires EDB_RPC_Server")
    config.addinivalue_line("markers", "slow: long-running test")
    config.addinivalue_line("markers", "smoke: minimal validation set")


# ---------------------------------------------------------------------------
# Skip logic for server-dependent tests
# ---------------------------------------------------------------------------


# Tests that are known to fail when using standard gRPC (--no-shared-memory) due to
# server-side behavioural differences in this transport mode.
_NO_SHM_XFAIL_NODEIDS = frozenset(
    [
        "tests/e2e/definition/test_multipole_debye_model.py::TestMultipoleDebyeModelParameters::test_parameters_empty_on_create",
        "tests/e2e/net/test_net_class.py::TestNetClassCreate::test_create_duplicate_name_raises",
        "tests/e2e/net/test_extended_net.py::TestExtendedNetCreate::test_create_duplicate_name_raises",
        "tests/e2e/net/test_differential_pair.py::TestDifferentialPairCreate::test_create_duplicate_name_raises",
    ]
)


def pytest_collection_modifyitems(config, items):
    if not _server_available():
        skip_marker = pytest.mark.skip(reason="ANSYS EDB server not available")
        for item in items:
            if "requires_server" in item.keywords:
                item.add_marker(skip_marker)

    if config.getoption("--no-shared-memory", default=False):
        xfail_marker = pytest.mark.xfail(
            reason="Known server-side failure over standard gRPC (--no-shared-memory)",
            strict=False,
        )
        for item in items:
            if item.nodeid in _NO_SHM_XFAIL_NODEIDS:
                item.add_marker(xfail_marker)


# ---------------------------------------------------------------------------
# Session-scoped fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def edb_session(request):
    """Launch an EDB server session for the entire test run.

    Skips all dependents if the server is unavailable.
    Pass ``--no-shared-memory`` on the pytest command line to disable
    shared-memory IPC and fall back to standard gRPC communication.
    Shared memory is enabled by default.
    """
    install_dir = _resolve_ansysem_install()
    if not install_dir or not Path(install_dir).is_dir():
        pytest.skip("ANSYS EDB server not available")
    use_shm = not request.config.getoption("--no-shared-memory", default=False)
    with session(install_dir, use_shared_memory_ipc=use_shm):
        yield


@pytest.fixture(scope="session")
def ansysem_install_dir(edb_session):
    """Return the resolved AnsysEM install directory as a Path.

    Guaranteed to be a valid directory (session is already running).
    """
    return Path(_resolve_ansysem_install())


@pytest.fixture(scope="session")
def asset_dir():
    """Return the path to the test assets root directory."""
    return Path(__file__).parent / "assets"


@pytest.fixture(scope="session")
def edb_dir(asset_dir):
    """Return the path to the EDB assets subdirectory."""
    return asset_dir / "edb"


@pytest.fixture(scope="session")
def xml_dir(asset_dir):
    """Return the path to the XML assets subdirectory."""
    return asset_dir / "xml"


# ---------------------------------------------------------------------------
# Function-scoped fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def edb_copy(edb_dir, tmp_path):
    """Factory fixture: copy an asset EDB to a temp directory and return the path.

    Usage::

        def test_something(edb_copy):
            edb_path = edb_copy("my_design.aedb")
            db = Database.open(str(edb_path), read_only=False)
    """

    def _copy(asset_name: str) -> Path:
        src = edb_dir / asset_name
        if not src.exists():
            pytest.fail(f"EDB asset not found: {src}")
        dst = tmp_path / asset_name
        shutil.copytree(src, dst)
        return dst

    return _copy


@pytest.fixture
def xml_asset_path(xml_dir):
    """Factory fixture: return the path to an XML/XSD asset file.

    XML assets are read-only and do not need to be copied.

    Usage::

        def test_something(xml_asset_path):
            path = xml_asset_path("tsv_gsg_tech.xml")
    """

    def _path(asset_name: str) -> Path:
        p = xml_dir / asset_name
        if not p.exists():
            pytest.fail(f"XML asset not found: {p}")
        return p

    return _path


@pytest.fixture
def new_db(edb_session, tmp_path):
    """Create a fresh empty database in a temp directory.

    Closes the database on teardown.
    """
    db_path = str(tmp_path / "test.aedb")
    db = Database.create(db_path)
    yield db
    db.close()


@pytest.fixture
def new_circuit_cell(new_db):
    """Create a circuit cell in the new database."""
    return Cell.create(new_db, CellType.CIRCUIT_CELL, "test_cell")


@pytest.fixture
def new_footprint_cell(new_db):
    """Create a footprint cell in the new database."""
    return Cell.create(new_db, CellType.FOOTPRINT_CELL, "test_footprint")


@pytest.fixture
def new_layout(new_circuit_cell):
    """Return the layout of the new circuit cell."""
    return new_circuit_cell.layout


# ---------------------------------------------------------------------------
# Asset-backed database fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def ssn_db(edb_session, edb_copy):
    """Open the SSN asset database read-only."""
    db_path = edb_copy("SSN.aedb")
    db = Database.open(str(db_path), read_only=True)
    yield db
    db.close()


@pytest.fixture
def diff_via_db(edb_session, edb_copy):
    """Open the Diff_Via asset database read-only."""
    db_path = edb_copy("Diff_Via.aedb")
    db = Database.open(str(db_path), read_only=True)
    yield db
    db.close()


@pytest.fixture
def db_with_definitions(edb_session, edb_copy):
    """Open the Definition_Types asset database read-only.

    Contains exactly one instance of each definition type (MaterialDef,
    PadstackDef, ComponentDef, PackageDef, DatasetDef, ApdBondwireDef,
    and one user-created Jedec4/5 alongside the server-injected Default).
    """
    db_path = edb_copy("Definition_Types.aedb")
    db = Database.open(str(db_path), read_only=True)
    yield db
    db.close()


# ---------------------------------------------------------------------------
# Temporary database factory fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def create_temp_db(edb_session, tmp_path):
    """Factory fixture: create a named empty database in the test's tmp_path.

    Automatically closes any unclosed databases on teardown.

    Usage::

        def test_something(create_temp_db):
            db = create_temp_db("my_test.aedb")
            ...
    """
    created = []

    def _create(name: str) -> Database:
        db = Database.create(str(tmp_path / name))
        created.append(db)
        return db

    yield _create

    for db in created:
        if not db.is_null:
            db.close()
