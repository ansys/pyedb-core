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

"""Tests for ansys.edb.core.database.Database."""

from pathlib import Path

import pytest

from ansys.edb.core.database import Database
from ansys.edb.core.database import ProductIdType
from ansys.edb.core.definition.bondwire_def import ApdBondwireDef
from ansys.edb.core.definition.bondwire_def import Jedec4BondwireDef
from ansys.edb.core.definition.bondwire_def import Jedec5BondwireDef
from ansys.edb.core.definition.component_def import ComponentDef
from ansys.edb.core.definition.dataset_def import DatasetDef
from ansys.edb.core.definition.material_def import MaterialDef
from ansys.edb.core.definition.package_def import PackageDef
from ansys.edb.core.definition.padstack_def import PadstackDef
from ansys.edb.core.layer.layer import LayerType
from ansys.edb.core.layer.stackup_layer import StackupLayer
from ansys.edb.core.layout.cell import Cell
from ansys.edb.core.primitive.rectangle import Rectangle
from ansys.edb.core.primitive.rectangle import RectangleRepresentationType

# ---------------------------------------------------------------------------
# Create / Open
# ---------------------------------------------------------------------------


@pytest.mark.requires_server
class TestDatabaseCreate:
    """Tests for Database.create() and Database.open()."""

    def test_create_returns_non_null_database(self, new_db):
        """Verify Database.create() returns a valid, non-null Database object."""
        assert not new_db.is_null

    def test_create_database_has_uid(self, new_db):
        """Verify a newly created database is assigned a non-zero unique EDB ID."""
        assert new_db.edb_uid > 0

    def test_create_fails_for_nonexistent_directory(self, edb_session, tmp_path):
        """Verify Database.create() raises when the path is completely invalid."""
        # Use a path with illegal characters that the OS itself will reject
        invalid_path = str(tmp_path / "invalid|path<>.aedb")
        with pytest.raises(RuntimeError):
            Database.create(invalid_path)

    @pytest.mark.parametrize("read_only", [True, False])
    def test_open_reflects_read_only_flag(self, edb_session, edb_copy, read_only):
        """Verify Database.open() reports is_read_only matching the flag passed to open()."""
        db_path = edb_copy("SSN.aedb")
        db = Database.open(str(db_path), read_only=read_only)
        try:
            assert db.is_read_only is read_only
        finally:
            db.close()

    def test_open_fails_for_nonexistent_path(self, edb_session, tmp_path):
        """Verify Database.open() raises when the path does not contain a database."""
        missing_path = str(tmp_path / "does_not_exist.aedb")
        with pytest.raises(RuntimeError):
            Database.open(missing_path, read_only=True)


# ---------------------------------------------------------------------------
# Core properties
# ---------------------------------------------------------------------------


@pytest.mark.requires_server
class TestDatabaseProperties:
    """Tests for Database instance properties."""

    def test_directory_matches_edb_path(self, create_temp_db, tmp_path):
        """Verify directory property returns the actual EDB directory path."""
        db = create_temp_db("dir_test.aedb")
        assert Path(db.directory) == Path(tmp_path / "dir_test.aedb")

    def test_version_matches_expected(self, diff_via_db):
        """Verify version property returns the expected version from the Diff_Via asset."""
        major, minor = diff_via_db.version
        assert major == 12
        assert minor == 1

    def test_string_property_round_trip(self, new_db):
        """Verify source property reflects the value assigned via its setter."""
        source_str = "my_source"
        new_db.source = source_str
        assert new_db.source == source_str

    def test_source_version_property_round_trip(self, new_db):
        """Verify source_version property reflects the value assigned via its setter."""
        source_version_str = "2024.2"
        new_db.source_version = source_version_str
        assert new_db.source_version == source_version_str


# ---------------------------------------------------------------------------
# Cell listing
# ---------------------------------------------------------------------------


@pytest.mark.requires_server
class TestDatabaseCells:
    """Tests for cell-listing properties of Database."""

    @pytest.mark.parametrize(
        "prop, fixture_name, expect_footprint",
        [
            ("circuit_cells", "new_circuit_cell", False),
            ("top_circuit_cells", "new_circuit_cell", False),
            ("footprint_cells", "new_footprint_cell", True),
        ],
    )
    def test_cell_list_count_and_type(self, request, new_db, prop, fixture_name, expect_footprint):
        """Verify each cell-listing property returns exactly one cell of the correct type."""
        request.getfixturevalue(fixture_name)  # ensure the cell fixture has been created
        cells = getattr(new_db, prop)
        assert isinstance(cells, list)
        assert len(cells) == 1
        cell = cells[0]
        assert isinstance(cell, Cell)
        assert cell.is_footprint is expect_footprint


# ---------------------------------------------------------------------------
# Definition object lists
# ---------------------------------------------------------------------------


@pytest.mark.requires_server
class TestDatabaseDefinitionLists:
    """Tests for definition-object listing properties with a dedicated asset."""

    @pytest.mark.parametrize(
        "prop, expected_count, expected_type",
        [
            ("material_defs", 1, MaterialDef),
            ("padstack_defs", 1, PadstackDef),
            ("component_defs", 1, ComponentDef),
            ("package_defs", 1, PackageDef),
            ("dataset_defs", 1, DatasetDef),
            ("apd_bondwire_defs", 1, ApdBondwireDef),
            ("jedec4_bondwire_defs", 2, Jedec4BondwireDef),
            ("jedec5_bondwire_defs", 2, Jedec5BondwireDef),
        ],
    )
    def test_definition_list_has_expected_objects(self, db_with_definitions, prop, expected_count, expected_type):
        """Verify each definition-list property has the expected count and type."""
        defs = getattr(db_with_definitions, prop)
        assert isinstance(defs, list)
        assert len(defs) == expected_count
        for d in defs:
            assert isinstance(d, expected_type)


# ---------------------------------------------------------------------------
# find_by_id
# ---------------------------------------------------------------------------


@pytest.mark.requires_server
class TestDatabaseFindById:
    """Tests for Database.find_by_id()."""

    def test_find_by_id(self, new_db):
        """Verify find_by_id() with a valid UID returns a non-null database with a matching UID."""
        uid = new_db.edb_uid
        found = Database.find_by_id(uid)
        assert not found.is_null
        assert found.edb_uid == uid

    def test_find_by_id_invalid_raises(self, edb_session):
        """Verify find_by_id() with a non-existent ID raises an exception.

        Note: find_by_id() does not document a Raises section; the server
        returns a database with an invalid/zero ID for an unknown UID, which
        trips the internal variable-owner-ID assertion in VariableServer.
        """
        with pytest.raises(AssertionError):
            Database.find_by_id(999999)


# ---------------------------------------------------------------------------
# save / save_as / close / delete
# ---------------------------------------------------------------------------


@pytest.mark.requires_server
class TestDatabasePersistence:
    """Tests for Database.save(), save_as(), close(), and delete()."""

    def test_save_persists_database_to_disk(self, new_db):
        """Verify save() writes the database directory to disk."""
        db_dir = new_db.directory
        new_db.save()
        assert Path(db_dir).exists()

    def test_save_as_creates_file_at_new_path(self, create_temp_db, tmp_path):
        """Verify save_as() writes the database to the specified new path."""
        db = create_temp_db("original.aedb")
        new_path = str(tmp_path / "copy.aedb")
        db.save_as(new_path)
        assert Path(new_path).exists()

    def test_save_as_with_version_sets_version(self, create_temp_db, tmp_path, edb_session):
        """Verify save_as() with a version string saves the database at the requested EDB version."""
        db = create_temp_db("versioned.aedb")
        new_path = str(tmp_path / "versioned_copy.aedb")
        db.save_as(new_path, version="5.1")
        saved_db = Database.open(new_path, read_only=True)
        try:
            major, minor = saved_db.version
            assert major == 5
            assert minor == 1
        finally:
            saved_db.close()

    def test_close_marks_database_as_null(self, create_temp_db):
        """Verify close() marks the database as null (id=0)."""
        db = create_temp_db("to_close.aedb")
        db.close()
        assert db.is_null

    def test_delete_removes_database(self, create_temp_db, tmp_path):
        """Verify Database.delete() completes without error."""
        db = create_temp_db("to_delete.aedb")
        dir = db.directory
        db.save()
        db.close()
        Database.delete(dir)
        assert not list(Path(dir).glob("*"))


# ---------------------------------------------------------------------------
# Product properties
# ---------------------------------------------------------------------------


@pytest.mark.requires_server
class TestDatabaseProductProperty:
    """Tests for product property get/set API."""

    def test_get_product_property_ids_returns_list(self, new_db):
        """Verify get_product_property_ids() returns a list after a property has been set."""
        prod_id = ProductIdType.HFSS_3D_LAYOUT
        new_db.set_product_property(prod_id, 1, "probe")
        ids = new_db.get_product_property_ids(prod_id)
        assert isinstance(ids, list)
        assert 1 in ids

    def test_set_and_get_product_property_round_trip(self, new_db):
        """Verify a value written with set_product_property is retrievable via get_product_property."""
        prod_id = ProductIdType.HFSS_3D_LAYOUT
        attr_id = 1
        expected = "test_value"
        new_db.set_product_property(prod_id, attr_id, expected)
        assert new_db.get_product_property(prod_id, attr_id) == expected


# ---------------------------------------------------------------------------
# copy_cells
# ---------------------------------------------------------------------------


@pytest.mark.requires_server
class TestDatabaseCopyCells:
    """Tests for Database.copy_cells()."""

    @pytest.mark.parametrize(
        "use_empty",
        [
            pytest.param(False, id="ssn_circuit_cells"),
            pytest.param(True, id="empty_list"),
        ],
    )
    def test_copy_cells(self, ssn_db, create_temp_db, use_empty):
        """Verify copy_cells() copies the expected cells into the target database.

        Parameters
        ----------
        use_empty : bool
            When True, copies an empty list (expects zero copied cells).
            When False, copies all circuit cells from the SSN asset (expects non-zero).
        """
        target_db = create_temp_db("target.aedb")
        cells_to_copy = [] if use_empty else ssn_db.circuit_cells
        source_count = len(cells_to_copy)
        copied = target_db.copy_cells(cells_to_copy)
        assert len(copied) == source_count
        assert len(target_db.circuit_cells) == source_count
        for cell in copied:
            assert isinstance(cell, Cell)


# ---------------------------------------------------------------------------
# import_material_from_control_file
# ---------------------------------------------------------------------------

# Materials defined in tests/e2e/assets/xml/tsv_gsg_tech.xml
_TSV_GSG_MATERIALS = frozenset(
    {
        "My_Oxyde_Middle",
        "air",
        "copper",
        "pec",
        "silicon1",
        "silicon_dioxide",
    }
)


@pytest.mark.requires_server
class TestDatabaseImportMaterial:
    """Tests for Database.import_material_from_control_file()."""

    @pytest.mark.parametrize(
        "use_schema, append",
        [
            pytest.param(False, True, id="no_schema_append"),
            pytest.param(False, False, id="no_schema_replace"),
            pytest.param(True, True, id="with_schema_append"),
            pytest.param(True, False, id="with_schema_replace"),
        ],
    )
    def test_import_material_from_control_file(self, new_db, xml_asset_path, ansysem_install_dir, use_schema, append):
        """Verify import_material_from_control_file() imports XML materials and respects append.

        Parameters
        ----------
        use_schema : bool
            When True, passes the AnsysEM install directory as schema_dir so the
            server can locate Control.xsd for validation.
        append : bool
            When True, pre-existing materials are kept alongside the imported ones.
            When False, pre-existing materials are removed before importing.
        """
        # Pre-create a sentinel material so we can verify the append behaviour.
        sentinel_name = "sentinel_material"
        MaterialDef.create(new_db, sentinel_name)
        assert any(m.name == sentinel_name for m in new_db.material_defs)

        control_file = str(xml_asset_path("tsv_gsg_tech.xml"))
        schema = str(ansysem_install_dir) if use_schema else None
        new_db.import_material_from_control_file(control_file, schema_dir=schema, append=append)

        imported_names = {m.name for m in new_db.material_defs}

        # All materials defined in the XML must be present regardless of append mode.
        assert _TSV_GSG_MATERIALS.issubset(imported_names), f"Missing materials: {_TSV_GSG_MATERIALS - imported_names}"

        # The sentinel should survive when append=True and be gone when append=False.
        if append:
            assert sentinel_name in imported_names, "append=True: pre-existing sentinel material should have been kept"
        else:
            assert sentinel_name not in imported_names, (
                "append=False: pre-existing sentinel material should have been removed"
            )


# ---------------------------------------------------------------------------
# scale
# ---------------------------------------------------------------------------


@pytest.mark.requires_server
class TestDatabaseScale:
    """Tests for Database.scale()."""

    def test_scale_modifies_geometry(self, new_db, new_circuit_cell):
        """Verify scale() actually scales geometry coordinates by the given factor."""
        layout = new_circuit_cell.layout

        # Add a signal layer for the rectangle
        layer = StackupLayer.create("TOP", LayerType.SIGNAL_LAYER, "0.035mm", "0mm", "copper")
        lc = layout.layer_collection
        lc.add_layer_top(layer)
        layout.layer_collection = lc

        # Create a rectangle with known coordinates (lower-left: 0,0; upper-right: 1mm, 2mm)
        rect = Rectangle.create(
            layout,
            "TOP",
            None,
            RectangleRepresentationType.LOWER_LEFT_UPPER_RIGHT,
            0.0,  # x lower-left
            0.0,  # y lower-left
            0.001,  # x upper-right (1mm in meters)
            0.002,  # y upper-right (2mm in meters)
            0.0,  # corner radius
            0.0,  # rotation
        )

        # Scale by factor of 2
        scale_factor = 2.0
        new_db.scale(scale_factor)

        # Verify coordinates have been scaled
        _, x1, y1, x2, y2, _, _ = rect.get_parameters()
        assert x1.double == pytest.approx(0.0)
        assert y1.double == pytest.approx(0.0)
        assert x2.double == pytest.approx(0.002)  # 1mm * 2
        assert y2.double == pytest.approx(0.004)  # 2mm * 2


# ---------------------------------------------------------------------------
# get_version_by_release
# ---------------------------------------------------------------------------


@pytest.mark.requires_server
class TestDatabaseGetVersionByRelease:
    """Tests for Database.get_version_by_release()."""

    def test_get_version_by_release(self, edb_session):
        """Verify get_version_by_release() returns a non-empty string for a known release."""
        version = Database.get_version_by_release("2020R1")
        assert version == "6.1"
