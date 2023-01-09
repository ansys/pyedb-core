"""Bondwire Definition."""

from enum import Enum

from ansys.api.edb.v1 import bondwire_def_pb2_grpc
import ansys.api.edb.v1.bondwire_def_pb2 as pb

from ansys.edb.core import ObjBase, messages
from ansys.edb.edb_defs import DefinitionObjType
from ansys.edb.session import StubAccessor, StubType
from ansys.edb.utility import Value


class _QueryBuilder:
    @staticmethod
    def bondwire_def_type(type):
        """Create a bondwire type message.

        Parameters
        ----------
        type : BondwireDefType

        Returns
        -------
        pb.BondwireDefTypeMessage
        """
        return pb.BondwireDefTypeMessage(
            type=type,
        )

    @staticmethod
    def bondwire_def_str_message(obj, string):
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


class BondwireDefType(Enum):
    """Enum representing bondwire types.

    - APD_BONDWIRE_DEF
       APD bondwire.
    - JEDEC4_BONDWIRE_DEF
       JEDEC4 bondwire.
    - JEDEC5_BONDWIRE_DEF
       JEDEC5 bondwire.
    """

    APD_BONDWIRE_DEF = pb.APD_BONDWIRE_DEF
    JEDEC4_BONDWIRE_DEF = pb.JEDEC4_BONDWIRE_DEF
    JEDEC5_BONDWIRE_DEF = pb.JEDEC5_BONDWIRE_DEF


class BondwireDef(ObjBase):
    """Class representing a bondwire definition."""

    __stub: bondwire_def_pb2_grpc.BondwireDefServiceStub = StubAccessor(StubType.bondwire_def)

    @property
    def definition_type(self):
        """:class:`DefinitionObjType`: type."""
        return DefinitionObjType.BONDWIRE_DEF

    @property
    def name(self):
        """:obj:`str`: Name of the bondwire definition.

        Read-Only.
        """
        return self.__stub.GetName(self.msg)

    def delete(self):
        """Delete a bondwire definition."""
        self.__stub.Delete(self.msg)


class ApdBondwireDef(BondwireDef):
    """Class representing an apd bondwire definition."""

    __stub: bondwire_def_pb2_grpc.ApdBondwireDefServiceStub = StubAccessor(
        StubType.apd_bondwire_def
    )

    @classmethod
    def create(cls, database, name):
        """Create an apd bondwire definition.

        Parameters
        ----------
        database : :class:`Database <ansys.edb.database.Database>`.
            Database in which Apd Bondwire definition will be searched.
        name : str
            Name of the Apd Bondwire definition.

        Returns
        -------
        ApdBondwireDef
            Apd Bondwire definition created.
        """
        bw_msg = cls.__stub.Create(_QueryBuilder.bondwire_def_str_message(database, name))
        return ApdBondwireDef(bw_msg)

    @classmethod
    def load_definitions_from_file(cls, database, name):
        """Load APD bondwire definition into the given database.

        Parameters
        ----------
        database : :class:`Database <ansys.edb.database.Database>`
            Database in which Apd Bondwire definition will be load.
        name : str
            Name of the Apd Bondwire definition.
        """
        cls.__stub.LoadDefinitionsFromFile(_QueryBuilder.bondwire_def_str_message(database, name))

    @classmethod
    def find_by_name(cls, database, name):
        """Find an apd bondwire definition by name into the given database.

        Parameters
        ----------
        database : :class:`Database <ansys.edb.database.Database>`
            Database in which Apd Bondwire definition will be searched.
        name : str
            Name of the Apd Bondwire definition.

        Returns
        -------
        ApdBondwireDef
            Apd Bondwire definition found.
        """
        return ApdBondwireDef(
            cls.__stub.FindByName(_QueryBuilder.bondwire_def_str_message(database, name))
        )

    def get_parameters(self):
        """Get parameters of an apd bondwire definition.

        Returns
        -------
        str
            String block of bondwire parameters.
        """
        return self.__stub.GetParameters(self.msg)

    def set_parameters(self, name):
        """Set parameters of an apd bondwire definition.

        Parameters
        ----------
        name : str
            String block of bondwire parameters.
        """
        self.__stub.SetParameters(_QueryBuilder.bondwire_def_str_message(self, name))

    @property
    def bondwire_type(self):
        """:class:`BondwireDefType`: Type of the apd bondwire definition.

        Read-Only.
        """
        return BondwireDefType.APD_BONDWIRE_DEF


class _Jedec4QueryBuilder:
    @staticmethod
    def jedec4_bondwire_def_set_parameters_message(j, top_to_die_distance):
        return pb.Jedec4BondwireDefSetParametersMessage(
            target=j.msg,
            top_to_die_distance=messages.value_message(top_to_die_distance),
        )


class Jedec4BondwireDef(BondwireDef):
    """Class representing a jedec 4 bondwire definition."""

    __stub: bondwire_def_pb2_grpc.Jedec4BondwireDefServiceStub = StubAccessor(
        StubType.jedec4_bondwire_def
    )

    @classmethod
    def create(cls, database, name):
        """Create a jedec 4 bondwire definition.

        Parameters
        ----------
        database : :class:`Database <ansys.edb.database.Database>`
            Database in which Jedec4 Bondwire definition will be created.
        name : str
            Name of the Jedec4 Bondwire definition.

        Returns
        -------
        Jedec4BondwireDef
            Jedec4 Bondwire definition created.
        """
        return Jedec4BondwireDef(
            cls.__stub.Create(_QueryBuilder.bondwire_def_str_message(database, name))
        )

    @classmethod
    def find_by_name(cls, database, name):
        """Find a jedec 4 bondwire definition by name.

        Parameters
        ----------
        database : :class:`Database <ansys.edb.database.Database>`
            Database in which Jedec4 Bondwire definition will be searched.
        name : str
            Name of the Jedec4 Bondwire definition.

        Returns
        -------
        Jedec4BondwireDef
            Jedec4 Bondwire definition found.
        """
        return Jedec4BondwireDef(
            cls.__stub.FindByName(_QueryBuilder.bondwire_def_str_message(database, name))
        )

    def get_parameters(self):
        """Get parameters of a jedec 4 bondwire definition.

        Returns
        -------
        :class:`Value <ansys.edb.utility.Value>`
            Bondwire top to die distance.
        """
        return Value(self.__stub.GetParameters(self.msg))

    def set_parameters(self, top_to_die_distance):
        """Set parameters of a jedec 4 bondwire definition.

        Parameters
        ----------
        top_to_die_distance : :class:`Value <ansys.edb.utility.Value>`
            Bondwire top to die distance.
        """
        self.__stub.SetParameters(
            _Jedec4QueryBuilder.jedec4_bondwire_def_set_parameters_message(
                self, top_to_die_distance
            )
        )

    @property
    def bondwire_type(self):
        """:class:`BondwireDefType`: Type of the jedec 4 bondwire definition.

        Read-Only.
        """
        return BondwireDefType.JEDEC4_BONDWIRE_DEF


class _Jedec5QueryBuilder:
    @staticmethod
    def jedec5_bondwire_def_parameters_message(top_to_die_distance, die_pad_angle, lead_pad_angle):
        return pb.Jedec5BondwireDefParametersMessage(
            top_to_die_distance=messages.value_message(top_to_die_distance),
            die_pad_angle=messages.value_message(die_pad_angle),
            lead_pad_angle=messages.value_message(lead_pad_angle),
        )

    @staticmethod
    def jedec5_bondwire_def_set_parameters_message(
        j,
        top_to_die_distance,
        die_pad_angle,
        lead_pad_angle,
    ):
        return pb.Jedec5BondwireDefSetParametersMessage(
            target=j.msg,
            parameters=_Jedec5QueryBuilder.jedec5_bondwire_def_parameters_message(
                top_to_die_distance, die_pad_angle, lead_pad_angle
            ),
        )


class Jedec5BondwireDef(BondwireDef):
    """Class representing a jedec 5 bondwire definition."""

    __stub: bondwire_def_pb2_grpc.Jedec5BondwireDefServiceStub = StubAccessor(
        StubType.jedec5_bondwire_def
    )

    @classmethod
    def create(cls, database, name):
        """Create a jedec 5 bondwire definition.

        Parameters
        ----------
        database : :class:`Database <ansys.edb.database.Database>`
            Database in which Jedec5 Bondwire definition will be created.
        name : str
            Name of the Jedec5 Bondwire definition.

        Returns
        -------
        Jedec5BondwireDef
            Jedec5 Bondwire definition created.
        """
        return Jedec5BondwireDef(
            cls.__stub.Create(_QueryBuilder.bondwire_def_str_message(database, name))
        )

    @classmethod
    def find_by_name(cls, database, name):
        """Find a jedec 5 bondwire definition by name.

        Parameters
        ----------
        database : :class:`Database <ansys.edb.database.Database>`
            Database in which Jedec5 Bondwire definition will be searched.
        name : str
            Name of the Jedec5 Bondwire definition.

        Returns
        -------
        Jedec5BondwireDef
            Jedec5 Bondwire definition found.
        """
        return Jedec5BondwireDef(
            cls.__stub.FindByName(_QueryBuilder.bondwire_def_str_message(database, name))
        )

    def get_parameters(self):
        """Get parameters of a jedec 5 bondwire definition.

        Returns
        -------
        tuple[
            :class:`Value <ansys.edb.utility.Value>`,
            :class:`Value <ansys.edb.utility.Value>`,
            :class:`Value <ansys.edb.utility.Value>`
        ]

            Returns a tuple of the following format:

            **(top_to_die_distance,die_pad_angle,lead_pad_angle)**

            **top_to_die_distance** : Bondwire top to die distance.

            **die_pad_angle** : Bondwire die pad angle.

            **lead_pad_angle** : Bondwire lead pad angle.
        """
        get_parameters_msg = self.__stub.GetParameters(self.msg)
        return (
            Value(get_parameters_msg.top_to_die_distance),
            Value(get_parameters_msg.die_pad_angle),
            Value(get_parameters_msg.lead_pad_angle),
        )

    def set_parameters(self, top_to_die_distance, die_pad_angle, lead_pad_angle):
        """Set parameters of a jedec 5 bondwire definition.

        Parameters
        ----------
        top_to_die_distance : :class:`Value <ansys.edb.utility.Value>`
            Bondwire top to die distance.
        die_pad_angle : :class:`Value <ansys.edb.utility.Value>`
            Bondwire die pad angle.
        lead_pad_angle : :class:`Value <ansys.edb.utility.Value>`
            Bondwire lead pad angle.
        """
        self.__stub.SetParameters(
            _Jedec5QueryBuilder.jedec5_bondwire_def_set_parameters_message(
                self, top_to_die_distance, die_pad_angle, lead_pad_angle
            )
        )

    @property
    def bondwire_type(self):
        """:class:`BondwireDefType`: Type of the jedec 5 bondwire definition.

        Read-Only.
        """
        return BondwireDefType.JEDEC5_BONDWIRE_DEF
