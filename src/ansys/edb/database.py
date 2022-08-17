"""Database."""

from enum import Enum

import ansys.api.edb.v1.database_pb2 as database_pb2
import ansys.api.edb.v1.edb_defs_pb2 as edb_defs_pb2
import google.protobuf.wrappers_pb2 as proto_wrappers

from ansys.edb.core import ObjBase, variable_server
from ansys.edb.core.messages import (
    double_property_message,
    edb_obj_collection_message,
    edb_obj_name_message,
    get_product_property_ids_message,
    get_product_property_message,
    set_product_property_message,
    str_message,
)
from ansys.edb.core.utils import map_list
from ansys.edb.definition import (
    ApdBondwireDef,
    BondwireDefType,
    ComponentDef,
    DatasetDef,
    Jedec4BondwireDef,
    Jedec5BondwireDef,
    MaterialDef,
    PackageDef,
    PadstackDef,
)
from ansys.edb.edb_defs import DefinitionObjType
from ansys.edb.layout import Cell
from ansys.edb.session import DatabaseServiceStub, StubAccessor, StubType


class ProductIdType(Enum):
    """Enum representing the ids of Ansys products that support EDB usage."""

    DESIGNER = edb_defs_pb2.DESIGNER
    SIWAVE = edb_defs_pb2.SI_WAVE
    GENERIC_TRANSLATOR = edb_defs_pb2.GENERIC_TRANSLATOR
    USER_DEFINED = edb_defs_pb2.USER_DEFINED
    INVALID_PRODUCT = edb_defs_pb2.INVALID_PRODUCT


class Database(ObjBase, variable_server.VariableServer):
    """Class representing a database object."""

    __stub: DatabaseServiceStub = StubAccessor(StubType.database)

    def __init__(self, msg):
        """Initialize a new Database.

        Parameters
        ----------
        msg : EDBObjMessage
        """
        ObjBase.__init__(self, msg)
        variable_server.VariableServer.__init__(self, msg)

    @classmethod
    def create(cls, db_path):
        """Create a database at the specified file location.

        Parameters
        ----------
        db_path : str

        Returns
        -------
        Database
        """
        return Database(cls.__stub.Create(proto_wrappers.StringValue(value=db_path)))

    @classmethod
    def open(cls, db_path, read_only):
        """Open an existing database at the specified file location.

        Parameters
        ----------
        db_path : str
        read_only : bool

        Returns
        -------
        Database
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
        """Delete a database at the specified file location.

        Parameters
        ----------
        db_path : str
        """
        cls.__stub.Delete(proto_wrappers.StringValue(value=db_path))

    def save(self):
        """Persist any changes into a file."""
        self.__stub.Save(self.msg)

    def close(self):
        """Close the database. Unsaved changes will be lost."""
        self.__stub.Close(self.msg)
        self.msg = None

    @staticmethod
    def _map_cell_edb_obj_collection(cells_msg):
        """Get a list of cell objects from the EDBObjCollection msg."""
        return map_list(cells_msg.items, Cell)

    @property
    def top_circuit_cells(self):
        """Get top circuit cells.

        Returns
        -------
        list of Cell
        """
        return Database._map_cell_edb_obj_collection(self.__stub.GetTopCircuits(self.msg))

    @property
    def circuit_cells(self):
        """Get all circuit cells.

        Returns
        -------
        list of Cell
        """
        return Database._map_cell_edb_obj_collection(self.__stub.GetCircuits(self.msg))

    @property
    def footprint_cells(self):
        """Get all footprint cells.

        Returns
        -------
        list of Cell
        """
        return Database._map_cell_edb_obj_collection(self.__stub.GetFootprints(self.msg))

    @property
    def edb_uid(self):
        """Get ID of the database.

        Returns
        -------
        int
        """
        return self.__stub.GetId(self.msg).value

    @property
    def is_read_only(self):
        """Determine if the database is open in a read-only mode.

        Returns
        -------
        bool
        """
        return self.__stub.IsReadOnly(self.msg).value

    @classmethod
    def find_by_id(cls, db_id):
        """Find a database by ID.

        Parameters
        ----------
        db_id : int

        Returns
        -------
        Database
        """
        return Database(cls.__stub.FindById(proto_wrappers.Int64Value(value=db_id)))

    def save_as(self, path, version=""):
        """Save this database to a new location.

        Parameters
        ----------
        path : str
        version : str
        """
        self.__stub.SaveAs(
            database_pb2.SaveAsDatabaseMessage(db=self.msg, new_location=path, version=version)
        )

    @classmethod
    def get_version_by_release(cls, release):
        """Get the EDB version corresponding to the given release name.

        Parameters
         ----------
         release : str

         Returns
         -------
         str
        """
        return cls.__stub.GetVersionByRelease(str_message(release)).value

    @property
    def directory(self):
        """Get the directory of the database.

        Returns
        -------
        str
        """
        return self.__stub.GetDirectory(self.msg).value

    def get_product_property(self, prod_id, attr_it):
        """Get the product property associated with the given product and attribute ids.

        Parameters
        ----------
        prod_id : ProductIdType
        attr_it : int

        Returns
        -------
        str
        """
        return self.__stub.GetProductProperty(
            get_product_property_message(self, prod_id, attr_it)
        ).value

    def set_product_property(self, prod_id, attr_it, prop_value):
        """Set the product property associated with the given product and attribute ids.

        Parameters
        ----------
        prod_id : ProductIdType
        attr_it : int
        prop_value : str
        """
        self.__stub.SetProductProperty(
            set_product_property_message(self, prod_id, attr_it, prop_value)
        )

    def get_product_property_ids(self, prod_id):
        """Get a list of attribute ids corresponding to the provided product id.

        Parameters
        ----------
        prod_id : ProductIdType

        Returns
        -------
        list[int]
        """
        attr_ids = self.__stub.GetProductPropertyIds(
            get_product_property_ids_message(self, prod_id)
        ).ids
        return [attr_id for attr_id in attr_ids]

    def import_material_from_control_file(self, control_file, schema_dir=None, append=True):
        """Import materials from the provided control file.

        Parameters
        ----------
        control_file : str
        schema_dir : str
        append : bool
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
        """Get version of the database.

        Returns
        -------
        tuple[int, int]
            Returns a tuple of the format [major, minor]
        """
        version_msg = self.__stub.GetVersion(self.msg)
        return version_msg.major.id, version_msg.minor.id

    def scale(self, scale_factor):
        """Scale all geometry in the database by the given scale factor.

        Parameters
        ----------
        scale_factor : float
        """
        self.__stub.Scale(double_property_message(self, scale_factor))

    @property
    def source(self):
        """Get source name of the database.

        Returns
        -------
        str
        """
        return self.__stub.GetSource(self.msg).value

    @source.setter
    def source(self, source):
        """Set source name of the database.

        Parameters
        ----------
        source : str
        """
        self.__stub.SetSource(edb_obj_name_message(self, source))

    @property
    def source_version(self):
        """Get source version of the database.

        Returns
        -------
        str
        """
        return self.__stub.GetSourceVersion(self.msg).value

    @source_version.setter
    def source_version(self, source_version):
        """Set source version of the database.

        Parameters
        ----------
        source_version : str
        """
        self.__stub.SetSourceVersion(edb_obj_name_message(self, source_version))

    def copy_cells(self, cells_to_copy):
        """Copy the given cells into this database.

        Parameters
        ----------
        cells_to_copy : list[Cell]
        """
        self.__stub.CopyCells(
            database_pb2.CopyCellsMessage(
                target=self.msg, cells=edb_obj_collection_message(cells_to_copy)
            )
        )

    def _get_definition_objs(self, def_class, def_type_enum, bw_def_type_enum=None):
        """Get the definition objects of the given type."""
        def_objs = self.__stub.GetDefinitionObjs(
            database_pb2.GetDefinitionObjsMessage(
                target=self.msg,
                type=def_type_enum.value,
                subtype=bw_def_type_enum.value if bw_def_type_enum is not None else None,
            )
        )
        return map_list(def_objs.items, def_class)

    def _get_bondwire_definition_objs(self, def_class, bw_def_type_enum):
        """Get the bondwire definition objects of the given type."""
        return self._get_definition_objs(
            def_class, DefinitionObjType.BONDWIRE_DEF, bw_def_type_enum
        )

    @property
    def apd_bondwire_defs(self):
        """Get all APD bondwire definitions in the database.

        Returns
        ----------
        list[ApdBondwireDef]
        """
        return self._get_bondwire_definition_objs(ApdBondwireDef, BondwireDefType.APD_BONDWIRE_DEF)

    @property
    def jedec4_bondwire_defs(self):
        """Get all JEDEC4 bondwire definitions in the database.

        Returns
        ----------
        list[Jedec4BondwireDef]
        """
        return self._get_bondwire_definition_objs(
            Jedec4BondwireDef, BondwireDefType.JEDEC4_BONDWIRE_DEF
        )

    @property
    def jedec5_bondwire_defs(self):
        """Get all JEDEC5 bondwire definitions in the database.

        Returns
        ----------
        list[Jedec5BondwireDef]
        """
        return self._get_bondwire_definition_objs(
            Jedec5BondwireDef, BondwireDefType.JEDEC5_BONDWIRE_DEF
        )

    @property
    def padstack_defs(self):
        """Get all Padstack definitions in the database.

        Returns
        ----------
        list[PadstackDef]
        """
        return self._get_definition_objs(PadstackDef, DefinitionObjType.PADSTACK_DEF)

    @property
    def package_defs(self):
        """Get all Package definitions in the database.

        Returns
        ----------
        list[PackageDef]
        """
        return self._get_definition_objs(PackageDef, DefinitionObjType.PACKAGE_DEF)

    @property
    def component_defs(self):
        """Get all component definitions in the database.

        Returns
        ----------
        list[ComponentDef]
        """
        return self._get_definition_objs(ComponentDef, DefinitionObjType.COMPONENT_DEF)

    @property
    def material_defs(self):
        """Get all material definitions in the database.

        Returns
        ----------
        list[MaterialDef]
        """
        return self._get_definition_objs(MaterialDef, DefinitionObjType.MATERIAL_DEF)

    @property
    def dataset_defs(self):
        """Get all dataset definitions in the database.

        Returns
        ----------
        list[DatasetDef]
        """
        return self._get_definition_objs(DatasetDef, DefinitionObjType.DATASET_DEF)
