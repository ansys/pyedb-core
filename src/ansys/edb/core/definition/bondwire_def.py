"""Bondwire definition."""

from enum import Enum

from ansys.api.edb.v1 import bondwire_def_pb2_grpc
import ansys.api.edb.v1.bondwire_def_pb2 as pb

from ansys.edb.core.edb_defs import DefinitionObjType
from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class BondwireDefType(Enum):
    """Enum representing different types of bondwires."""

    APD_BONDWIRE_DEF = pb.APD_BONDWIRE_DEF
    JEDEC4_BONDWIRE_DEF = pb.JEDEC4_BONDWIRE_DEF
    JEDEC5_BONDWIRE_DEF = pb.JEDEC5_BONDWIRE_DEF


class BondwireDef(ObjBase):
    """Represents a bondwire definition."""

    __stub: bondwire_def_pb2_grpc.BondwireDefServiceStub = StubAccessor(StubType.bondwire_def)

    @property
    def definition_type(self):
        """:class:`.DefinitionObjType`: Object type of the bondwire definition."""
        return DefinitionObjType.BONDWIRE_DEF

    @property
    def name(self):
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
    def create(cls, database, name):
        """Create an APD bondwire definition in a given database.

        Parameters
        ----------
        database : :class:`.Database`
            Database to create the APD bondwire definition in.
        name : str
            Name of the APD bondwire definition.

        Returns
        -------
        ApdBondwireDef
            APD bondwire definition created.
        """
        bw_msg = cls.__stub.Create(BondwireDef._bondwire_def_str_message(database, name))
        return ApdBondwireDef(bw_msg)

    @classmethod
    def load_definitions_from_file(cls, database, name):
        """Load an APD bondwire definition into a given database.

        Parameters
        ----------
        database : :class:`.Database`
            Database to load the APD bondwire into.
        name : str
            Name of the APD bondwire definition.
        """
        cls.__stub.LoadDefinitionsFromFile(BondwireDef._bondwire_def_str_message(database, name))

    @classmethod
    def find_by_name(cls, database, name):
        """Find an APD bondwire definition by name in a given database.

        Parameters
        ----------
        database : :class:`.Database`
            Database to search for the APD bondwire definition.
        name : str
            Name of the APD bondwire definition.

        Returns
        -------
        ApdBondwireDef
            APD bondwire definition found.
        """
        return ApdBondwireDef(
            cls.__stub.FindByName(BondwireDef._bondwire_def_str_message(database, name))
        )

    def get_parameters(self):
        """Get the parameters of the APD bondwire definition.

        Returns
        -------
        str
            String block of the bondwire parameters.
        """
        return self.__stub.GetParameters(self.msg)

    def set_parameters(self, name):
        """Set parameters of the APD bondwire definition.

        Parameters
        ----------
        name : str
            String block of the bondwire parameters.
        """
        self.__stub.SetParameters(BondwireDef._bondwire_def_str_message(self, name))

    @property
    def bondwire_type(self):
        """:class:`BondwireDefType`: Type of the APD bondwire.

        This property is read-only.
        """
        return BondwireDefType.APD_BONDWIRE_DEF


class Jedec4BondwireDef(BondwireDef):
    """Represents a JEDEC4 bondwire definition."""

    __stub: bondwire_def_pb2_grpc.Jedec4BondwireDefServiceStub = StubAccessor(
        StubType.jedec4_bondwire_def
    )

    @classmethod
    def create(cls, database, name):
        """Create a JEDEC4 bondwire definition.

        Parameters
        ----------
        database : :class:`.Database`
            Database to create the JEDEC4 bondwire definition in.
        name : str
            Name of the JEDEC4 bondwire definition.

        Returns
        -------
        Jedec4BondwireDef
            JEDEC4 bondwire definition created.
        """
        return Jedec4BondwireDef(
            cls.__stub.Create(BondwireDef._bondwire_def_str_message(database, name))
        )

    @classmethod
    def find_by_name(cls, database, name):
        """Find a JEDEC4 bondwire definition by name in a given database.

        Parameters
        ----------
        database : :class:`.Database`
            Database to search for the JEDEC4 bondwire definition.
        name : str
            Name of the JEDEC4 bondwire definition.

        Returns
        -------
        Jedec4BondwireDef
            JEDEC4 bondwire definition found.
        """
        return Jedec4BondwireDef(
            cls.__stub.FindByName(BondwireDef._bondwire_def_str_message(database, name))
        )

    def get_parameters(self):
        """Get parameters of the JEDEC4 bondwire definition.

        Returns
        -------
        :class:`.Value`
            Bondwire top-to-die distance.
        """
        return Value(self.__stub.GetParameters(self.msg))

    def set_parameters(self, top_to_die_distance):
        """Set parameters of the JEDEC4 bondwire definition.

        Parameters
        ----------
        top_to_die_distance : :class:`.Value`
            Bondwire top-to-die distance.
        """
        self.__stub.SetParameters(
            pb.Jedec4BondwireDefSetParametersMessage(
                target=self.msg, top_to_die_distance=messages.value_message(top_to_die_distance)
            )
        )

    @property
    def bondwire_type(self):
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
    def create(cls, database, name):
        """Create a JEDEC5 bondwire definition.

        Parameters
        ----------
        database : :class:`.Database`
            Database to create the JEDEC5 bondwire definition in.
        name : str
            Name of the JEDEC5 bondwire definition.

        Returns
        -------
        Jedec5BondwireDef
            JEDEC5 bondwire definition created.
        """
        return Jedec5BondwireDef(
            cls.__stub.Create(BondwireDef._bondwire_def_str_message(database, name))
        )

    @classmethod
    def find_by_name(cls, database, name):
        """Find a JEDEC5 bondwire definition by name in a given database.

        Parameters
        ----------
        database : :class:`.Database`
            Database to search for the JEDEC5 bondwire definition.
        name : str
            Name of the JEDEC5 bondwire definition.

        Returns
        -------
        Jedec5BondwireDef
            JEDEC5 bondwire definition found.
        """
        return Jedec5BondwireDef(
            cls.__stub.FindByName(BondwireDef._bondwire_def_str_message(database, name))
        )

    def get_parameters(self):
        """Get parameters of the JEDEC5 bondwire definition.

        Returns
        -------
        tuple[:class:`.Value`, :class:`.Value`, :class:`.Value`]
            The tuple is in this format: ``(top_to_die_distance,die_pad_angle,lead_pad_angle)``

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

    def set_parameters(self, top_to_die_distance, die_pad_angle, lead_pad_angle):
        """Set parameters of the JEDEC5 bondwire definition.

        Parameters
        ----------
        top_to_die_distance : :class:`.Value`
            Bondwire top-to-die distance.
        die_pad_angle : :class:`.Value`
            Bondwire die pad angle.
        lead_pad_angle : :class:`.Value`
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
    def bondwire_type(self):
        """:class:`BondwireDefType`: Type of the JEDEC5 bondwire.

        This property is read-only.
        """
        return BondwireDefType.JEDEC5_BONDWIRE_DEF
