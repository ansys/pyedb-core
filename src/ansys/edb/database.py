"""Database."""

from enum import Enum

import ansys.api.edb.v1.database_pb2 as database_pb2
import ansys.api.edb.v1.edb_defs_pb2 as edb_defs_pb2
import google.protobuf.wrappers_pb2 as proto_wrappers

from ansys.edb.core import ObjBase, variable_server
from ansys.edb.layout import Cell
from ansys.edb.session import get_database_stub


class ProductIdType(Enum):
    """Enum representing the ids of Ansys products that support EDB usage."""

    DESIGNER = edb_defs_pb2.DESIGNER
    SIWAVE = edb_defs_pb2.SI_WAVE
    GENERIC_TRANSLATOR = edb_defs_pb2.GENERIC_TRANSLATOR
    USER_DEFINED = edb_defs_pb2.USER_DEFINED
    INVALID_PRODUCT = edb_defs_pb2.INVALID_PRODUCT


class Database(ObjBase, variable_server.VariableServer):
    """Class representing a database object."""

    def __init__(self, msg):
        """Initialize a new Database.

        Parameters
        ----------
        msg : EDBObjMessage
        """
        ObjBase.__init__(self, msg)
        variable_server.VariableServer.__init__(self, msg)

    @staticmethod
    def create(db_path):
        """Create a database at the specified file location.

        Parameters
        ----------
        db_path : str

        Returns
        -------
        Database
        """
        return Database(get_database_stub().Create(proto_wrappers.StringValue(value=db_path)))

    @staticmethod
    def open(db_path, read_only):
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
            get_database_stub().Open(
                database_pb2.OpenDatabaseMessage(
                    edb_path=proto_wrappers.StringValue(value=db_path),
                    read_only=proto_wrappers.BoolValue(value=read_only),
                )
            )
        )

    @staticmethod
    def delete(db_path):
        """Delete a database at the specified file location.

        Parameters
        ----------
        db_path : str

        Returns
        -------
        bool
        """
        return get_database_stub().Delete(proto_wrappers.StringValue(value=db_path)).value

    def save(self):
        """Persist any changes into a file.

        Returns
        -------
        bool
        """
        return get_database_stub().Save(self.msg).value

    def close(self):
        """Close the database. Unsaved changes will be lost.

        Returns
        -------
        bool
        """
        close_success = get_database_stub().Close(self.msg).value
        if close_success:
            self.msg = None
        return close_success

    @property
    def top_circuit_cells(self):
        """Get circuit cells.

        Returns
        -------
        list of Cell
        """
        return [Cell(edb_obj) for edb_obj in get_database_stub().GetTopCircuits(self.msg).items]

    def get_id(self):
        """Get ID of the database.

        Returns
        -------
        int
        """
        return get_database_stub().GetId(self.msg).value

    def is_read_only(self):
        """Determine if the database is open in a read-only mode.

        Returns
        -------
        bool
        """
        return get_database_stub().IsReadOnly(self.msg).value

    @staticmethod
    def find_by_id(db_id):
        """Find a database by ID.

        Parameters
        ----------
        db_id : int

        Returns
        -------
        Database
        """
        return Database(get_database_stub().FindById(proto_wrappers.Int64Value(value=db_id)))
