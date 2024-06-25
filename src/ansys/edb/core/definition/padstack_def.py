"""Padstack definition."""

from ansys.api.edb.v1 import padstack_def_pb2_grpc
import ansys.api.edb.v1.padstack_def_pb2 as pb

from ansys.edb.core.definition.padstack_def_data import PadstackDefData
from ansys.edb.core.edb_defs import DefinitionObjType
from ansys.edb.core.inner import ObjBase
from ansys.edb.core.session import StubAccessor, StubType


class PadstackDef(ObjBase):
    """Represents a padstack definition."""

    __stub: padstack_def_pb2_grpc.PadstackDefServiceStub = StubAccessor(StubType.padstack_def)

    @classmethod
    def create(cls, db, name):
        """Create a padstack definition in a given database.

        Parameters
        ----------
        db : :class:`.Database`
            Database to create the padstack definition in.
        name : str
            Data to set on the padstack definition.

        Returns
        -------
        PadstackDef
            Padstack definition created.
        """
        return PadstackDef(cls.__stub.Create(PadstackDef._padstack_def_string_message(db, name)))

    @classmethod
    def find_by_name(cls, db, name):
        """Find a padstack definition by name in a given database.

        Parameters
        ----------
        db : :class:`.Database`.
            Database to search for the padstack definition.
        name : str
            Name of the padstack definition.

        Returns
        -------
        PadstackDef
            Padstack definition found.
        """
        return PadstackDef(
            cls.__stub.FindByName(PadstackDef._padstack_def_string_message(db, name))
        )

    @property
    def definition_type(self):
        """:class:`.DefinitionObjType`: Definition type."""
        return DefinitionObjType.PADSTACK_DEF

    @property
    def name(self):
        """:obj:`str`: Name of the padstack definition.

        This property is read-only.
        """
        return self.__stub.GetName(self.msg).value

    @property
    def data(self):
        """:class:`.PadstackDefData`: \
        Data for the padstack definition."""
        return PadstackDefData(self.__stub.GetData(self.msg))

    @data.setter
    def data(self, data):
        self.__stub.SetData(pb.PadstackDefSetDataMessage(target=self.msg, data=data.msg))

    def delete(self):
        """Delete the padstack definition."""
        self.__stub.Delete(self.msg)

    @staticmethod
    def _padstack_def_string_message(target, name):
        """Create a string message for the padstack definition.

        Parameters
        ----------
        target : :class:`.Database` or PadstackDef
        name : str
           Name of the string message.

        Returns
        -------
        PadstackDefStringMessage
        """
        return pb.PadstackDefStringMessage(target=target.msg, name=name)
