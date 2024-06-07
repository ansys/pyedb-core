"""Database."""

from enum import Enum

import ansys.api.edb.v1.database_pb2 as database_pb2
import ansys.api.edb.v1.edb_defs_pb2 as edb_defs_pb2
import google.protobuf.wrappers_pb2 as proto_wrappers

from ansys.edb.core.definition.bondwire_def import (
    ApdBondwireDef,
    BondwireDefType,
    Jedec4BondwireDef,
    Jedec5BondwireDef,
)
from ansys.edb.core.definition.component_def import ComponentDef
from ansys.edb.core.definition.dataset_def import DatasetDef
from ansys.edb.core.definition.material_def import MaterialDef
from ansys.edb.core.definition.package_def import PackageDef
from ansys.edb.core.definition.padstack_def import PadstackDef
from ansys.edb.core.edb_defs import DefinitionObjType
from ansys.edb.core.inner import ObjBase, variable_server
from ansys.edb.core.inner.messages import (
    double_property_message,
    edb_obj_collection_message,
    edb_obj_name_message,
    get_product_property_ids_message,
    get_product_property_message,
    set_product_property_message,
    str_message,
)
from ansys.edb.core.inner.utils import map_list
from ansys.edb.core.layout.cell import Cell
from ansys.edb.core.session import DatabaseServiceStub, StubAccessor, StubType


class ProductIdType(Enum):
    """Provides an enum representing IDs of Ansys products that support EDB usage."""

    HFSS_3D_LAYOUT = DESIGNER = edb_defs_pb2.DESIGNER
    SIWAVE = edb_defs_pb2.SI_WAVE
    GENERIC_TRANSLATOR = edb_defs_pb2.GENERIC_TRANSLATOR
    USER_DEFINED = edb_defs_pb2.USER_DEFINED
    INVALID_PRODUCT = edb_defs_pb2.INVALID_PRODUCT


class Database(ObjBase, variable_server.VariableServer):
    """Represents a database object."""

    __stub: DatabaseServiceStub = StubAccessor(StubType.database)

    def __init__(self, msg):
        """Initialize a new database.

        Parameters
        ----------
        msg : EDBObjMessage
        """
        ObjBase.__init__(self, msg)
        variable_server.VariableServer.__init__(self, msg)

    @classmethod
    def create(cls, db_path):
        """Create a database in a given location.

        Parameters
        ----------
        db_path : str
            Path to the top-level database directory.

        Returns
        -------
        Database
        """
        msg = cls.__stub.Create(proto_wrappers.StringValue(value=db_path))
        return Database(msg)

    @classmethod
    def open(cls, db_path, read_only):
        """Open a database in a given location.

        Parameters
        ----------
        db_path : str
            Path to the top-level database directory.
        read_only : bool
            Whether to open the database in read-only mode.

        Returns
        -------
        Database object or None
            Database object opened or ``None`` if no database object is found.
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
    def delete(cls, db_path):
        """Delete a database in a given specified location.

        Parameters
        ----------
        db_path : str
            Path to the top-level database directory.
        """
        cls.__stub.Delete(proto_wrappers.StringValue(value=db_path))

    def save(self):
        """Save any changes to the database."""
        self.__stub.Save(self.msg)

    def close(self):
        """Close the database.

        .. note::
            Unsaved changes are lost.
        """
        self.__stub.Close(self.msg)
        self.msg = None

    @staticmethod
    def _map_cell_edb_obj_collection(cells_msg):
        """Get a list of cell objects from the ``EDBObjCollection`` message."""
        return map_list(cells_msg.items, Cell)

    @property
    def top_circuit_cells(self):
        """:obj:`list` of :class:`.Cell`: Top circuit cells in the database."""
        return Database._map_cell_edb_obj_collection(self.__stub.GetTopCircuits(self.msg))

    @property
    def circuit_cells(self):
        """:obj:`list` of :class:`.Cell`: All circuit cells in the database."""
        return Database._map_cell_edb_obj_collection(self.__stub.GetCircuits(self.msg))

    @property
    def footprint_cells(self):
        """:obj:`list` of :class:`.Cell`: All footprint cells in the database."""
        return Database._map_cell_edb_obj_collection(self.__stub.GetFootprints(self.msg))

    @property
    def edb_uid(self):
        """:obj:`int`: Unique EDB ID of the database."""
        return self.__stub.GetId(self.msg).value

    @property
    def is_read_only(self):
        """:obj:`bool`: Flag indicating if the database is open in read-only mode."""
        return self.__stub.IsReadOnly(self.msg).value

    @classmethod
    def find_by_id(cls, db_id):
        """Find a database by ID.

        Parameters
        ----------
        db_id : int
            Unique EDB ID for the database.

        Returns
        -------
        Database
            Database when successful, Null when failed.
        """
        return Database(cls.__stub.FindById(proto_wrappers.Int64Value(value=db_id)))

    def save_as(self, path, version=""):
        """Save the database to a new location and older EDB version.

        Parameters
        ----------
        path : str
            Location for saving the new database file to.
        version : str, default: ""
            EDB version for the new database file. The default is ``""``, in which case
            the new database file is saved for the current version.
        """
        self.__stub.SaveAs(
            database_pb2.SaveAsDatabaseMessage(db=self.msg, new_location=path, version=version)
        )

    @classmethod
    def get_version_by_release(cls, release):
        """Get the EDB version for a given release name.

        Parameters
        ----------
        release : str
           Release name.

        Returns
        -------
        str
           EDB version.
        """
        return cls.__stub.GetVersionByRelease(str_message(release)).value

    @property
    def directory(self):
        """:obj:`str`: Directory where the database is located."""
        return self.__stub.GetDirectory(self.msg).value

    def get_product_property(self, prod_id, attr_it):
        """Get a product-specific property value.

        Parameters
        ----------
        prod_id : ProductIdType
            Product ID.
        attr_it : int
            Attribute ID.

        Returns
        -------
        str
            Property value.
        """
        return self.__stub.GetProductProperty(
            get_product_property_message(self, prod_id, attr_it)
        ).value

    def set_product_property(self, prod_id, attr_it, prop_value):
        """Set the product property associated with the given product ID and attribute ID.

        Parameters
        ----------
        prod_id : ProductIdType
            Product ID.
        attr_it : int
            Attribute ID.
        prop_value : str
            New value for the product property.
        """
        self.__stub.SetProductProperty(
            set_product_property_message(self, prod_id, attr_it, prop_value)
        )

    def get_product_property_ids(self, prod_id):
        """Get a list of attribute IDs for a given product property ID.

        Parameters
        ----------
        prod_id : ProductIdType
            Product ID.

        Returns
        -------
        list[int]
            Attribute IDs associated with the product property.
        """
        attr_ids = self.__stub.GetProductPropertyIds(
            get_product_property_ids_message(self, prod_id)
        ).ids
        return [attr_id for attr_id in attr_ids]

    def import_material_from_control_file(self, control_file, schema_dir=None, append=True):
        """Import materials from a control file.

        Parameters
        ----------
        control_file : str
            Full path to the control file.
        schema_dir : str
            Path to the schema directory.
        append : bool, default: True
            Whether to keep existing materials in the database. If ``False``, the
            existing materials in the database are removed.
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
    def version(self):
        """:obj:`tuple` of (:obj:`int`, :obj:`int`): Version [major, minor] of the database."""
        version_msg = self.__stub.GetVersion(self.msg)
        return version_msg.major.id, version_msg.minor.id

    def scale(self, scale_factor):
        """Scale all geometries and their locations uniformly by a positive factor.

        Parameters
        ----------
        scale_factor : float
            Amount to multiply coordinates by.
        """
        self.__stub.Scale(double_property_message(self, scale_factor))

    @property
    def source(self):
        """:obj:`str`: Name of the source database."""
        return self.__stub.GetSource(self.msg).value

    @source.setter
    def source(self, source):
        self.__stub.SetSource(edb_obj_name_message(self, source))

    @property
    def source_version(self):
        """:obj:`str`: Source version for the database."""
        return self.__stub.GetSourceVersion(self.msg).value

    @source_version.setter
    def source_version(self, source_version):
        self.__stub.SetSourceVersion(edb_obj_name_message(self, source_version))

    def copy_cells(self, cells_to_copy):
        """Copy cells from other databases or this database into this database.

        Parameters
        ----------
        cells_to_copy : list[:class:`.Cell`]
            Cells to copy.

        Returns
        -------
        list[:class:`.Cell`]
            New cells created in this database.
        """
        return Database._map_cell_edb_obj_collection(
            self.__stub.CopyCells(
                database_pb2.CopyCellsMessage(
                    target=self.msg, cells=edb_obj_collection_message(cells_to_copy)
                )
            )
        )

    def _get_definition_objs(self, def_class, def_type_enum, bw_def_type_enum=None):
        """Get the definition objects of a given type."""
        def_objs = self.__stub.GetDefinitionObjs(
            database_pb2.GetDefinitionObjsMessage(
                target=self.msg,
                type=def_type_enum.value,
                subtype=bw_def_type_enum.value if bw_def_type_enum is not None else None,
            )
        )
        return map_list(def_objs.items, def_class)

    def _get_bondwire_definition_objs(self, def_class, bw_def_type_enum):
        """Get the bondwire definition objects of a given type."""
        return self._get_definition_objs(
            def_class, DefinitionObjType.BONDWIRE_DEF, bw_def_type_enum
        )

    @property
    def apd_bondwire_defs(self):
        """:obj:`list` of :class:`.ApdBondwireDef`: All APD bondwire definitions in the database."""
        return self._get_bondwire_definition_objs(ApdBondwireDef, BondwireDefType.APD_BONDWIRE_DEF)

    @property
    def jedec4_bondwire_defs(self):
        """:obj:`list` of :class:`.Jedec4BondwireDef`: All JEDEC4 bondwire definitions in the database."""
        return self._get_bondwire_definition_objs(
            Jedec4BondwireDef, BondwireDefType.JEDEC4_BONDWIRE_DEF
        )

    @property
    def jedec5_bondwire_defs(self):
        """:obj:`list` of:class:`.Jedec5BondwireDef`: All JEDEC5 bondwire definitions in the database."""
        return self._get_bondwire_definition_objs(
            Jedec5BondwireDef, BondwireDefType.JEDEC5_BONDWIRE_DEF
        )

    @property
    def padstack_defs(self):
        """:obj:`list` of :class:`.PadstackDef`: All padstack definitions in the database."""
        return self._get_definition_objs(PadstackDef, DefinitionObjType.PADSTACK_DEF)

    @property
    def package_defs(self):
        """:obj:`list` of :class:`.PackageDef`: All package definitions in the database."""
        return self._get_definition_objs(PackageDef, DefinitionObjType.PACKAGE_DEF)

    @property
    def component_defs(self):
        """:obj:`list` of :class:`.ComponentDef`: All component definitions in the database."""
        return self._get_definition_objs(ComponentDef, DefinitionObjType.COMPONENT_DEF)

    @property
    def material_defs(self):
        """:obj:`list` of :class:`.MaterialDef`: All material definitions in the database."""
        return self._get_definition_objs(MaterialDef, DefinitionObjType.MATERIAL_DEF)

    @property
    def dataset_defs(self):
        """:obj:`list` of :class:`.DatasetDef`: All dataset definitions in the database."""
        return self._get_definition_objs(DatasetDef, DefinitionObjType.DATASET_DEF)
