"""Padstack Definition."""

from ansys.api.edb.v1 import padstack_def_pb2_grpc
import ansys.api.edb.v1.padstack_def_pb2 as pb

from ansys.edb.core import ObjBase
from ansys.edb.definition.padstack_def_data import PadstackDefData
from ansys.edb.session import StubAccessor, StubType


class _PadstackDefQueryBuilder:
    """Class for creating grpc messages of PadstackDef."""

    @staticmethod
    def padstack_def_string_message(target, name):
        """Create a PadstackDefStringMessage.

        Parameters
        ----------
        target: :class:`Database <ansys.edb.database.Database>` or PadstackDef
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
        data : :class:`PadstackDefData <ansys.edb.definition.padstack_def_data.PadstackDefData>`
            PadstackDefData data to be set on the PadstackDef

        Returns
        -------
        PadstackDefSetDataMessage
        """
        return pb.PadstackDefSetDataMessage(target=target.msg, data=data.msg)


class PadstackDef(ObjBase):
    """Class representing a padstack definition."""

    __stub: padstack_def_pb2_grpc.PadstackDefServiceStub = StubAccessor(StubType.padstack_def)

    @classmethod
    def create(cls, db, name):
        """Create a PadstackDef object.

        Parameters
        ----------
        db: :class:`Database <ansys.edb.database.Database>`
            Database object which will create the PadstackDef.
        name : str
            Data to be set on the PadstackDef.

        Returns
        -------
        PadstackDef
            PadstackDef that was created in the given database.
        """
        return PadstackDef(
            cls.__stub.Create(_PadstackDefQueryBuilder.padstack_def_string_message(db, name))
        )

    def delete(self):
        """Delete a PadstackDef."""
        self.__stub.Delete(self.msg)

    @classmethod
    def find_by_name(cls, db, name):
        """Find a PadstackDef by name.

        Parameters
        ----------
        db: :class:`Database <ansys.edb.database.Database>`.
            Database in which we search for the PadstackDef.
        name : str
            Name of PadstackDef.

        Returns
        -------
        PadstackDef
        """
        return PadstackDef(
            cls.__stub.FindByName(_PadstackDefQueryBuilder.padstack_def_string_message(db, name))
        )

    @property
    def name(self):
        """Get Name of a PadstackDef.

        Returns
        -------
        str
            Name of the PadstackDef.
        """
        return self.__stub.GetName(self.msg).value

    @property
    def data(self):
        """Get PadstackDefData of a PadstackDef.

        Returns
        -------
        :class:`PadstackDefData <ansys.edb.definition.padstack_def_data.PadstackDefData>`
            PadstackDefData of the PadstackDef.
        """
        return PadstackDefData(self.__stub.GetData(self.msg))

    @data.setter
    def data(self, data):
        """Set PadstackDefData of a PadstackDef."""
        self.__stub.SetData(_PadstackDefQueryBuilder.padstack_def_set_data_message(self, data))
