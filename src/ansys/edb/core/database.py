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

"""Database."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.inner.messages import EDBObjMessage

from enum import Enum

import ansys.api.edb.v1.database_pb2 as database_pb2
import ansys.api.edb.v1.edb_defs_pb2 as edb_defs_pb2
import google.protobuf.wrappers_pb2 as proto_wrappers

from ansys.edb.core.definition.bondwire_def import ApdBondwireDef
from ansys.edb.core.definition.bondwire_def import BondwireDefType
from ansys.edb.core.definition.bondwire_def import Jedec4BondwireDef
from ansys.edb.core.definition.bondwire_def import Jedec5BondwireDef
from ansys.edb.core.definition.component_def import ComponentDef
from ansys.edb.core.definition.dataset_def import DatasetDef
from ansys.edb.core.definition.material_def import MaterialDef
from ansys.edb.core.definition.package_def import PackageDef
from ansys.edb.core.definition.padstack_def import PadstackDef
from ansys.edb.core.edb_defs import DefinitionObjType
from ansys.edb.core.inner import ObjBase
from ansys.edb.core.inner import variable_server
from ansys.edb.core.inner.messages import double_property_message
from ansys.edb.core.inner.messages import edb_obj_collection_message
from ansys.edb.core.inner.messages import edb_obj_name_message
from ansys.edb.core.inner.messages import get_product_property_ids_message
from ansys.edb.core.inner.messages import get_product_property_message
from ansys.edb.core.inner.messages import set_product_property_message
from ansys.edb.core.inner.messages import str_message
from ansys.edb.core.inner.utils import map_list
from ansys.edb.core.layout.cell import Cell
from ansys.edb.core.session import DatabaseServiceStub
from ansys.edb.core.session import StubAccessor
from ansys.edb.core.session import StubType


class ProductIdType(Enum):
    """Ansys products that can read and write product-specific properties on a database."""

    HFSS_3D_LAYOUT = DESIGNER = edb_defs_pb2.DESIGNER
    """HFSS 3D Layout."""
    SIWAVE = edb_defs_pb2.SI_WAVE
    """SIwave."""
    GENERIC_TRANSLATOR = edb_defs_pb2.GENERIC_TRANSLATOR
    """A generic translator product."""
    USER_DEFINED = edb_defs_pb2.USER_DEFINED
    """A user-defined product."""
    INVALID_PRODUCT = edb_defs_pb2.INVALID_PRODUCT
    """Sentinel value indicating no product is set."""


class Database(ObjBase, variable_server.VariableServer):
    """Represents an EDB database.

    A database is the top-level container for designs. It is stored as an
    ``.aedb`` folder on disk and holds one or more cells along with the
    definitions (padstacks, materials, components, and so on) shared by
    those cells.
    """

    __stub: DatabaseServiceStub = StubAccessor(StubType.database)

    def __init__(self, msg: EDBObjMessage):
        """Initialize a new database.

        Parameters
        ----------
        msg : .EDBObjMessage
        """
        ObjBase.__init__(self, msg)
        variable_server.VariableServer.__init__(self, self)

    @classmethod
    def create(cls, db_path: str) -> Database:
        """Create a new database at a location.

        Parameters
        ----------
        db_path : str
            Path to the ``.aedb`` folder to create for the new database.

        Returns
        -------
        .Database
            Newly created database.

        Raises
        ------
        RuntimeError
            If the path is not accessible or the database could not be created there.
        """
        msg = cls.__stub.Create(proto_wrappers.StringValue(value=db_path))
        return Database(msg)

    @classmethod
    def open(cls, db_path: str, read_only: bool) -> Database:
        """Open an existing database from a location.

        Parameters
        ----------
        db_path : str
            Path to the ``.aedb`` folder of the database to open.
        read_only : bool
            Whether to open the database in read-only mode. When ``False``, the
            database is opened for writing.

        Returns
        -------
        .Database
            Database opened from the given location.

        Raises
        ------
        RuntimeError
            If the path is not accessible, the database uses an unsupported layout
            component format, or the database is encrypted.
        """
        return Database(
            cls.__stub.Open(
                database_pb2.OpenDatabaseMessage(
                    edb_path=db_path,
                    read_only=read_only,
                )
            )
        )

    @classmethod
    def delete(cls, db_path: str):
        """Delete a database from disk.

        Parameters
        ----------
        db_path : str
            Path to the ``.aedb`` folder of the database to delete.

        Raises
        ------
        RuntimeError
            If the database at the given path could not be deleted.
        """
        cls.__stub.Delete(proto_wrappers.StringValue(value=db_path))

    def save(self):
        """Save any changes made to the database.

        Raises
        ------
        RuntimeError
            If the database could not be saved.
        """
        self.__stub.Save(self.msg)

    def close(self):
        """Close the database.

        .. note::
            Unsaved changes are lost when the database is closed.

        Raises
        ------
        RuntimeError
            If the database could not be closed.
        """
        self.__stub.Close(self.msg)
        self.msg = None

    @staticmethod
    def _map_cell_edb_obj_collection(cells_msg: EDBObjMessage) -> list[Cell]:
        """Get a list of cell objects from the :class:`.EDBObjCollection` message."""
        return map_list(cells_msg.items, Cell)

    @property
    def top_circuit_cells(self) -> list[Cell]:
        """:obj:`list` of :class:`.Cell`: Top-level circuit cells in the database."""
        return Database._map_cell_edb_obj_collection(self.__stub.GetTopCircuits(self.msg))

    @property
    def circuit_cells(self) -> list[Cell]:
        """:obj:`list` of :class:`.Cell`: All circuit cells in the database."""
        return Database._map_cell_edb_obj_collection(self.__stub.GetCircuits(self.msg))

    @property
    def footprint_cells(self) -> list[Cell]:
        """:obj:`list` of :class:`.Cell`: All footprint cells in the database."""
        return Database._map_cell_edb_obj_collection(self.__stub.GetFootprints(self.msg))

    @property
    def edb_uid(self) -> int:
        """:obj:`int`: Unique ID assigned to the database."""
        return self.__stub.GetId(self.msg).value

    @property
    def is_read_only(self) -> bool:
        """:obj:`bool`: Flag indicating if the database is open in read-only mode."""
        return self.__stub.IsReadOnly(self.msg).value

    @classmethod
    def find_by_id(cls, db_id: int) -> Database:
        """Find a previously opened database by its unique ID.

        Parameters
        ----------
        db_id : int
            Unique ID of the database to find.

        Returns
        -------
        .Database
            Database with the given unique ID.
        """
        return Database(cls.__stub.FindById(proto_wrappers.Int64Value(value=db_id)))

    def save_as(self, path: str, version: str = ""):
        """Save the database to a new location, optionally in an older version format.

        Parameters
        ----------
        path : str
            Path to the ``.aedb`` folder where the database is saved.
        version : str, default: ""
            EDB version to save the database as. If empty, the current version is used.
        """
        self.__stub.SaveAs(database_pb2.SaveAsDatabaseMessage(db=self.msg, new_location=path, version=version))

    @classmethod
    def get_version_by_release(cls, release: str) -> str:
        """Get the EDB version associated with a release name.

        Parameters
        ----------
        release : str
           Release name whose EDB version is requested.

        Returns
        -------
        str
           EDB version associated with the release name.
        """
        return cls.__stub.GetVersionByRelease(str_message(release)).value

    @property
    def directory(self) -> str:
        """:obj:`str`: Directory containing the database."""
        return self.__stub.GetDirectory(self.msg).value

    def get_product_property(self, prod_id: ProductIdType, attr_it: int) -> str:
        """Get a product-specific property value stored on the database.

        Parameters
        ----------
        prod_id : .ProductIdType
            Product the property belongs to.
        attr_it : int
            Attribute ID of the property to get.

        Returns
        -------
        str
            Value of the product property.
        """
        return self.__stub.GetProductProperty(get_product_property_message(self, prod_id, attr_it)).value

    def set_product_property(self, prod_id: ProductIdType, attr_it: int, prop_value: str):
        """Set a product-specific property value on the database.

        Parameters
        ----------
        prod_id : .ProductIdType
            Product the property belongs to.
        attr_it : int
            Attribute ID of the property to set.
        prop_value : str
            New value for the product property.
        """
        self.__stub.SetProductProperty(set_product_property_message(self, prod_id, attr_it, prop_value))

    def get_product_property_ids(self, prod_id: ProductIdType) -> list[int]:
        """Get the attribute IDs of the product properties stored on the database.

        Parameters
        ----------
        prod_id : .ProductIdType
            Product whose property attribute IDs are requested.

        Returns
        -------
        list of int
            Attribute IDs of the product properties associated with the given product.
        """
        attr_ids = self.__stub.GetProductPropertyIds(get_product_property_ids_message(self, prod_id)).ids
        return [attr_id for attr_id in attr_ids]

    def import_material_from_control_file(self, control_file: str, schema_dir: str | None = None, append: bool = True):
        """Import materials into the database from a control file.

        Parameters
        ----------
        control_file : str
            Path to the control file to import materials from.
        schema_dir : str or None, default: None
            Path to the schema directory used to validate the control file. When not set,
            the schema in the Ansys EM install directory is used.
        append : bool, default: True
            When true, existing materials in the database are kept. When false, existing
            materials are removed before the import.

        Raises
        ------
        RuntimeError
            If the materials could not be imported from the control file.
        """
        self.__stub.ImportMaterialFromControlFile(
            database_pb2.ImportMaterialFromControlFileMessage(
                target=self.msg,
                file=control_file,
                schema_path=schema_dir,
                append=append,
            )
        )

    @property
    def version(self) -> tuple[int, int]:
        """:obj:`tuple` of (:obj:`int`, :obj:`int`): Major and minor version numbers of the database."""
        version_msg = self.__stub.GetVersion(self.msg)
        return version_msg.major.id, version_msg.minor.id

    def scale(self, scale_factor: float):
        """Scale the geometry of the database.

        Parameters
        ----------
        scale_factor : float
            Positive factor that all geometry coordinates in the database are multiplied by.

        Raises
        ------
        RuntimeError
            If the geometry could not be scaled.
        """
        self.__stub.Scale(double_property_message(self, scale_factor))

    @property
    def source(self) -> str:
        """:obj:`str`: Name of the source database the database was derived from."""
        return self.__stub.GetSource(self.msg).value

    @source.setter
    def source(self, source: str):
        self.__stub.SetSource(edb_obj_name_message(self, source))

    @property
    def source_version(self) -> str:
        """:obj:`str`: Version of the source the database was derived from."""
        return self.__stub.GetSourceVersion(self.msg).value

    @source_version.setter
    def source_version(self, source_version: str):
        self.__stub.SetSourceVersion(edb_obj_name_message(self, source_version))

    def copy_cells(self, cells_to_copy: list[Cell]) -> list[Cell]:
        """Copy cells from another database into this database.

        Parameters
        ----------
        cells_to_copy : list of .Cell
            Cells to copy into the database.

        Returns
        -------
        list of .Cell
            New cells created in the database.

        Raises
        ------
        RuntimeError
            If no cells were copied.
        """
        return Database._map_cell_edb_obj_collection(
            self.__stub.CopyCells(
                database_pb2.CopyCellsMessage(target=self.msg, cells=edb_obj_collection_message(cells_to_copy))
            )
        )

    def _get_definition_objs(
        self, def_class, def_type_enum: DefinitionObjType, bw_def_type_enum: BondwireDefType = None
    ) -> list:
        """Get the definition objects of a given type."""
        def_objs = self.__stub.GetDefinitionObjs(
            database_pb2.GetDefinitionObjsMessage(
                target=self.msg,
                type=def_type_enum.value,
                subtype=bw_def_type_enum.value if bw_def_type_enum is not None else None,
            )
        )
        return map_list(def_objs.items, def_class)

    def _get_bondwire_definition_objs(self, def_class, bw_def_type_enum: BondwireDefType) -> list:
        """Get the bondwire definition objects of a given type."""
        return self._get_definition_objs(def_class, DefinitionObjType.BONDWIRE_DEF, bw_def_type_enum)

    @property
    def apd_bondwire_defs(self) -> list[ApdBondwireDef]:
        """:obj:`list` of :class:`.ApdBondwireDef`: All APD bondwire definitions in the database."""
        return self._get_bondwire_definition_objs(ApdBondwireDef, BondwireDefType.APD_BONDWIRE_DEF)

    @property
    def jedec4_bondwire_defs(self) -> list[Jedec4BondwireDef]:
        """:obj:`list` of :class:`.Jedec4BondwireDef`: All JEDEC4 bondwire definitions in the database."""
        return self._get_bondwire_definition_objs(Jedec4BondwireDef, BondwireDefType.JEDEC4_BONDWIRE_DEF)

    @property
    def jedec5_bondwire_defs(self) -> list[Jedec5BondwireDef]:
        """:obj:`list` of :class:`.Jedec5BondwireDef`: All JEDEC5 bondwire definitions in the database."""
        return self._get_bondwire_definition_objs(Jedec5BondwireDef, BondwireDefType.JEDEC5_BONDWIRE_DEF)

    @property
    def padstack_defs(self) -> list[PadstackDef]:
        """:obj:`list` of :class:`.PadstackDef`: All padstack definitions in the database."""
        return self._get_definition_objs(PadstackDef, DefinitionObjType.PADSTACK_DEF)

    @property
    def package_defs(self) -> list[PackageDef]:
        """:obj:`list` of :class:`.PackageDef`: All package definitions in the database."""
        return self._get_definition_objs(PackageDef, DefinitionObjType.PACKAGE_DEF)

    @property
    def component_defs(self) -> list[ComponentDef]:
        """:obj:`list` of :class:`.ComponentDef`: All component definitions in the database."""
        return self._get_definition_objs(ComponentDef, DefinitionObjType.COMPONENT_DEF)

    @property
    def material_defs(self) -> list[MaterialDef]:
        """:obj:`list` of :class:`.MaterialDef`: All material definitions in the database."""
        return self._get_definition_objs(MaterialDef, DefinitionObjType.MATERIAL_DEF)

    @property
    def dataset_defs(self) -> list[DatasetDef]:
        """:obj:`list` of :class:`.DatasetDef`: All dataset definitions in the database."""
        return self._get_definition_objs(DatasetDef, DefinitionObjType.DATASET_DEF)
