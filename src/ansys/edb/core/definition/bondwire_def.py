"""Bondwire definition."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.database import Database
    from ansys.edb.core.typing import ValueLike

from enum import Enum

from ansys.api.edb.v1 import bondwire_def_pb2_grpc
import ansys.api.edb.v1.bondwire_def_pb2 as pb

from ansys.edb.core.edb_defs import DefinitionObjType
from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class BondwireDefType(Enum):
    """Enum representing different types of bondwire definitions."""

    APD_BONDWIRE_DEF = pb.APD_BONDWIRE_DEF
    JEDEC4_BONDWIRE_DEF = pb.JEDEC4_BONDWIRE_DEF
    JEDEC5_BONDWIRE_DEF = pb.JEDEC5_BONDWIRE_DEF


class BondwireDef(ObjBase):
    """Represents a bondwire definition."""

    __stub: bondwire_def_pb2_grpc.BondwireDefServiceStub = StubAccessor(StubType.bondwire_def)

    @property
    def definition_type(self) -> DefinitionObjType:
        """:class:`.DefinitionObjType`: Definition object type of the bondwire definition."""
        return DefinitionObjType.BONDWIRE_DEF

    @property
    def name(self) -> str:
        """:obj:`str`: Name of the bondwire definition.

        This property is read-only.
        """
        return self.__stub.GetName(self.msg)

    def delete(self):
        """Delete the bondwire definition."""
        self.__stub.Delete(self.msg)

    @staticmethod
    def _bondwire_def_str_message(obj, string):
        """Create a bondwire definition string message.

        Parameters
        ----------
        obj : Union[Database, 'ApdBondwireDef', 'Jedec4BondwireDef', 'Jedec5BondwireDef']
        string : str

        Returns
        -------
        pb.BondwireDefStrMessage
        """
        return pb.BondwireDefStrMessage(object=obj.msg, name=string)


class ApdBondwireDef(BondwireDef):
    """Represents an APD bondwire definition."""

    __stub: bondwire_def_pb2_grpc.ApdBondwireDefServiceStub = StubAccessor(
        StubType.apd_bondwire_def
    )

    @classmethod
    def create(cls, database: Database, name: str) -> ApdBondwireDef:
        """Create an APD bondwire definition in a given database.

        Parameters
        ----------
        database : .Database
            Database to create the APD bondwire definition in.
        name : str
            Name of the APD bondwire definition.

        Returns
        -------
        .ApdBondwireDef
        """
        bw_msg = cls.__stub.Create(BondwireDef._bondwire_def_str_message(database, name))
        return ApdBondwireDef(bw_msg)

    @classmethod
    def load_definitions_from_file(cls, database: Database, name: str):
        """Load APD bondwire definitions into a given database from the provided XML file.

        Parameters
        ----------
        database : .Database
            Database to load the APD bondwire definitions into.
        name : str
            File path of the XML file to be imported.
        """
        cls.__stub.LoadDefinitionsFromFile(BondwireDef._bondwire_def_str_message(database, name))

    @classmethod
    def find_by_name(cls, database: Database, name: str) -> ApdBondwireDef:
        """Find an APD bondwire definition by name in a given database.

        Parameters
        ----------
        database : .Database
            Database to search for the APD bondwire definition in.
        name : str
            Name of the APD bondwire definition.

        Returns
        -------
        .ApdBondwireDef
            APD bondwire definition found. \
            If an APD bondwire definition isn't found, the returned APD bondwire definition is :meth:`null <.is_null>`.
        """
        return ApdBondwireDef(
            cls.__stub.FindByName(BondwireDef._bondwire_def_str_message(database, name))
        )

    def get_parameters(self) -> str:
        """Get the parameters of the APD bondwire definition.

        Returns
        -------
        str
            String block of the bondwire parameters.
        """
        return self.__stub.GetParameters(self.msg)

    def set_parameters(self, name: str):
        """Set the parameters of the APD bondwire definition.

        Parameters
        ----------
        name : str
            String block of the bondwire parameters.
        """
        self.__stub.SetParameters(BondwireDef._bondwire_def_str_message(self, name))

    @property
    def bondwire_type(self) -> BondwireDefType:
        """:class:`.BondwireDefType`: Type of the APD bondwire.

        This property is read-only.
        """
        return BondwireDefType.APD_BONDWIRE_DEF


class Jedec4BondwireDef(BondwireDef):
    """Represents a JEDEC4 bondwire definition."""

    __stub: bondwire_def_pb2_grpc.Jedec4BondwireDefServiceStub = StubAccessor(
        StubType.jedec4_bondwire_def
    )

    @classmethod
    def create(cls, database: Database, name: str) -> Jedec4BondwireDef:
        """Create a JEDEC4 bondwire definition.

        Parameters
        ----------
        database : .Database
            Database to create the JEDEC4 bondwire definition in.
        name : str
            Name of the JEDEC4 bondwire definition.

        Returns
        -------
        .Jedec4BondwireDef
        """
        return Jedec4BondwireDef(
            cls.__stub.Create(BondwireDef._bondwire_def_str_message(database, name))
        )

    @classmethod
    def find_by_name(cls, database: Database, name: str) -> Jedec4BondwireDef:
        """Find a JEDEC4 bondwire definition by name in a given database.

        Parameters
        ----------
        database : .Database
            Database to search for the JEDEC4 bondwire definition.
        name : str
            Name of the JEDEC4 bondwire definition.

        Returns
        -------
        .Jedec4BondwireDef
            JEDEC4 bondwire definition found. \
            If an JEDEC4 bondwire definition isn't found, the returned JEDEC4 bondwire definition \
            is :meth:`null <.is_null>`.
        """
        return Jedec4BondwireDef(
            cls.__stub.FindByName(BondwireDef._bondwire_def_str_message(database, name))
        )

    def get_parameters(self) -> Value:
        """Get the parameters of the JEDEC4 bondwire definition.

        Returns
        -------
        .Value
            Bondwire top-to-die distance.
        """
        return Value(self.__stub.GetParameters(self.msg))

    def set_parameters(self, top_to_die_distance: ValueLike):
        """Set the parameters of the JEDEC4 bondwire definition.

        Parameters
        ----------
        top_to_die_distance : :term:`ValueLike`
            Bondwire top-to-die distance.
        """
        self.__stub.SetParameters(
            pb.Jedec4BondwireDefSetParametersMessage(
                target=self.msg, top_to_die_distance=messages.value_message(top_to_die_distance)
            )
        )

    @property
    def bondwire_type(self) -> BondwireDefType:
        """:class:`BondwireDefType`: Type of the JEDEC4 bondwire.

        This property is read-only.
        """
        return BondwireDefType.JEDEC4_BONDWIRE_DEF


class Jedec5BondwireDef(BondwireDef):
    """Represents a JEDEC5 bondwire definition."""

    __stub: bondwire_def_pb2_grpc.Jedec5BondwireDefServiceStub = StubAccessor(
        StubType.jedec5_bondwire_def
    )

    @classmethod
    def create(cls, database: Database, name: str) -> Jedec5BondwireDef:
        """Create a JEDEC5 bondwire definition.

        Parameters
        ----------
        database : .Database
            Database to create the JEDEC5 bondwire definition in.
        name : str
            Name of the JEDEC5 bondwire definition.

        Returns
        -------
        .Jedec5BondwireDef
            JEDEC5 bondwire definition created.
        """
        return Jedec5BondwireDef(
            cls.__stub.Create(BondwireDef._bondwire_def_str_message(database, name))
        )

    @classmethod
    def find_by_name(cls, database: Database, name: str) -> Jedec5BondwireDef:
        """Find a JEDEC5 bondwire definition by name in a given database.

        Parameters
        ----------
        database : .Database
            Database to search for the JEDEC5 bondwire definition.
        name : str
            Name of the JEDEC5 bondwire definition.

        Returns
        -------
        .Jedec5BondwireDef
            JEDEC5 bondwire definition found. \
            If an JEDEC5 bondwire definition isn't found, the returned JEDEC5 bondwire definition is \
            :meth:`null <.is_null>`.
        """
        return Jedec5BondwireDef(
            cls.__stub.FindByName(BondwireDef._bondwire_def_str_message(database, name))
        )

    def get_parameters(self) -> tuple[Value, Value, Value]:
        """Get parameters of the JEDEC5 bondwire definition.

        Returns
        -------
        tuple of .Value, .Value, .Value
            The tuple is in this format: ``(top_to_die_distance, die_pad_angle, lead_pad_angle)``

            - ``top_to_die_distance``: Bondwire top-to-die distance.
            - ``die_pad_angle``: Bondwire die pad angle.
            - ``lead_pad_angle``: Bondwire lead pad angle.
        """
        get_parameters_msg = self.__stub.GetParameters(self.msg)
        return (
            Value(get_parameters_msg.top_to_die_distance),
            Value(get_parameters_msg.die_pad_angle),
            Value(get_parameters_msg.lead_pad_angle),
        )

    def set_parameters(
        self, top_to_die_distance: ValueLike, die_pad_angle: ValueLike, lead_pad_angle: ValueLike
    ):
        """Set parameters of the JEDEC5 bondwire definition.

        Parameters
        ----------
        top_to_die_distance : :term:`ValueLike`
            Bondwire top-to-die distance.
        die_pad_angle : :term:`ValueLike`
            Bondwire die pad angle.
        lead_pad_angle : :term:`ValueLike`
            Bondwire lead pad angle.
        """
        self.__stub.SetParameters(
            pb.Jedec5BondwireDefSetParametersMessage(
                target=self.msg,
                parameters=pb.Jedec5BondwireDefParametersMessage(
                    top_to_die_distance=messages.value_message(top_to_die_distance),
                    die_pad_angle=messages.value_message(die_pad_angle),
                    lead_pad_angle=messages.value_message(lead_pad_angle),
                ),
            )
        )

    @property
    def bondwire_type(self) -> BondwireDefType:
        """:class:`BondwireDefType`: Type of the JEDEC5 bondwire.

        This property is read-only.
        """
        return BondwireDefType.JEDEC5_BONDWIRE_DEF
