"""Padstack Definition."""

import ansys.api.edb.v1.padstack_def_pb2 as pb

from ...session import get_padstack_def_stub
from ...utility.edb_errors import handle_grpc_exception
from ..base import ObjBase
from .padstack_def_data import PadstackDefData


class _PadstackDefQueryBuilder:
    """Class for creating grpc messages of PadstackDef."""

    @staticmethod
    def padstack_def_string_message(target, name):
        """Create a PadstackDefStringMessage.

        Parameters
        ----------
        target: Database or PadstackDef
        name : str

        Returns
        -------
        PadstackDefStringMessage
        """
        return pb.PadstackDefStringMessage(target=target.msg, name=name)

    @staticmethod
    def padstack_def_set_data_message(target, data):
        """Create a PadstackDefSetDataMessage.

        Parameters
        ----------
        target: PadstackDef
            PadstackDef target to change.
        data : PadstackDefData
            PadstackDefData data to be set on the PadstackDef

        Returns
        -------
        PadstackDefSetDataMessage
        """
        return pb.PadstackDefSetDataMessage(target=target.msg, data=data.msg)


class PadstackDef(ObjBase):
    """Class representing a padstack definition."""

    @staticmethod
    @handle_grpc_exception
    def create(db, name):
        """Create a PadstackDef object.

        Parameters
        ----------
        db: Database
            Database object which will create the PadstackDef.
        name : str
            Data to be set on the PadstackDef

        Returns
        -------
        PadstackDef
        """
        return PadstackDef(
            get_padstack_def_stub().Create(
                _PadstackDefQueryBuilder.padstack_def_string_message(db, name)
            )
        )

    @handle_grpc_exception
    def delete(self):
        """Delete a PadstackDef."""
        get_padstack_def_stub().Delete(self.msg)

    @staticmethod
    @handle_grpc_exception
    def find_by_name(db, name):
        """Find a PadstackDef by name.

        Parameters
        ----------
        db: Database.
        name : str
            Name of PadstackDef.

        Returns
        -------
        PadstackDef
        """
        return PadstackDef(
            get_padstack_def_stub().FindByName(
                _PadstackDefQueryBuilder.padstack_def_string_message(db, name)
            )
        )

    @property
    @handle_grpc_exception
    def name(self):
        """Get Name of a PadstackDef.

        Returns
        -------
        str
        """
        return get_padstack_def_stub().GetName(self.msg).value

    @property
    @handle_grpc_exception
    def data(self):
        """Get PadstackDefData of a PadstackDef.

        Returns
        -------
        PadstackDefData
        """
        return PadstackDefData(get_padstack_def_stub().GetData(self.msg))

    @data.setter
    @handle_grpc_exception
    def data(self, data):
        """Set PadstackDefData of a PadstackDef.

        Parameters
        ----------
        data : PadstackDefData
            PadstackDefData data object to be set on the PadstackDef.
        """
        get_padstack_def_stub().SetData(
            _PadstackDefQueryBuilder.padstack_def_set_data_message(self, data)
        )
