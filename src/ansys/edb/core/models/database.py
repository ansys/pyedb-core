"""Database."""

import ansys.api.edb.v1.database_pb2 as database_pb2
import google.protobuf.wrappers_pb2 as proto_wrappers

from ..session import get_database_stub
from ..utility.edb_errors import handle_grpc_exception
from .base import ObjBase
from .cell.cell import Cell


class Database(ObjBase):
    """Class representing a database object."""

    @staticmethod
    @handle_grpc_exception
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
    @handle_grpc_exception
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
    @handle_grpc_exception
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

    @handle_grpc_exception
    def save(self):
        """Persist any changes into a file.

        Returns
        -------
        bool
        """
        return get_database_stub().Save(self._msg).value

    @handle_grpc_exception
    def close(self):
        """Close the session without persisting the changes."""
        close_success = get_database_stub().Close(self._msg).value
        if close_success:
            self._msg.impl_ptr_address = 0
        return close_success

    @property
    @handle_grpc_exception
    def top_circuit_cells(self):
        """Get circuit cells.

        Returns
        -------
        list of Cell
        """
        return iter(
            [
                Cell(edb_obj)
                for edb_obj in get_database_stub().GetTopCircuits(self._msg).edb_obj_collection
            ]
        )

    @handle_grpc_exception
    def get_id(self):
        """Get ID of the database.

        Returns
        -------
        int
        """
        return get_database_stub().GetId(self._msg).value

    @handle_grpc_exception
    def is_read_only(self):
        """Determine if the database is open in a read-only mode.

        Returns
        -------
        bool
        """
        return get_database_stub().IsReadOnly(self._msg).value

    @staticmethod
    @handle_grpc_exception
    def find_by_id(db_id):
        """Find a database by ID.

        Parameters
        ----------
        db_id : str

        Returns
        -------
        Database
        """
        return Database(get_database_stub().FindById(proto_wrappers.Int64Value(value=db_id)))
