"""Bondwire Definition."""

from enum import Enum

import ansys.api.edb.v1.bondwire_def_pb2 as pb

from ansys.edb.core.core import ObjBase, messages
from ansys.edb.core.session import (
    get_apd_bondwire_def_stub,
    get_bondwire_def_stub,
    get_jedec4_bondwire_def_stub,
    get_jedec5_bondwire_def_stub,
)
from ansys.edb.core.utility import Value


class BondwireDefType(Enum):
    """Enum representing bondwire types."""

    APD_BONDWIRE_DEF = pb.APD_BONDWIRE_DEF
    JEDEC4_BONDWIRE_DEF = pb.JEDEC4_BONDWIRE_DEF
    JEDEC5_BONDWIRE_DEF = pb.JEDEC5_BONDWIRE_DEF


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


class BondwireDef(ObjBase):
    """Class representing a bondwire definition."""

    def delete(self):
        """Delete a bondwire definition."""
        get_bondwire_def_stub().Delete(self.msg)

    @property
    def name(self):
        """Return the name of the bondwire definition.

        Returns
        -------
        str
        """
        return get_bondwire_def_stub().GetName(self.msg)


class ApdBondwireDef(BondwireDef):
    """Class representing an apd bondwire definition."""

    @staticmethod
    def create(database, name):
        """Create an apd bondwire definition.

        Parameters
        ----------
        database: Database,
        name: str

        Returns
        -------
        ApdBondwireDef
        """
        bw_msg = get_apd_bondwire_def_stub().Create(
            _QueryBuilder.bondwire_def_str_message(database, name)
        )
        return ApdBondwireDef(bw_msg)

    def load_definitions_from_file(database, name):
        """Create an apd bondwire definition.

        Parameters
        ----------
        database: Database,
        name: str
        """
        get_apd_bondwire_def_stub().LoadDefinitionsFromFile(
            _QueryBuilder.bondwire_def_str_message(database, name)
        )

    def find_by_name(database, name):
        """Find an apd bondwire definition by name.

        Parameters
        ----------
        database: Database,
        name: str

        Returns
        -------
        ApdBondwireDef
        """
        return ApdBondwireDef(
            get_apd_bondwire_def_stub().FindByName(
                _QueryBuilder.bondwire_def_str_message(database, name)
            )
        )

    def get_parameters(self):
        """Get parameters of an apd bondwire definition.

        Returns
        -------
        str
        """
        return get_apd_bondwire_def_stub().GetParameters(self.msg)

    def set_parameters(self, name):
        """Set parameters of an apd bondwire definition.

        Parameters
        ----------
        name: str
        """
        get_apd_bondwire_def_stub().SetParameters(
            _QueryBuilder.bondwire_def_str_message(self, name)
        )

    @property
    def bondwire_type(self):
        """Return apd bondwire type.

        Returns
        -------
        BondwireDefType
        """
        return BondwireDefType.APD_BONDWIRE_DEF


class _Jedec4QueryBuilder:
    @staticmethod
    def jedec4_bondwire_def_set_parameters_message(j, top_to_die_distance):
        return pb.Jedec4BondwireDefSetParametersMessage(
            target=j.msg,
            top_to_die_distance=messages.value_message(top_to_die_distance),
        )


class Jedec4BondwireDef(ObjBase):
    """Class representing a jedec 4 bondwire definition."""

    @staticmethod
    def create(database, name):
        """Create a jedec 4 bondwire definition.

        Parameters
        ----------
        database: Database,
        name: str

        Returns
        -------
        Jedec4BondwireDef
        """
        return Jedec4BondwireDef(
            get_jedec4_bondwire_def_stub().Create(
                _QueryBuilder.bondwire_def_str_message(database, name)
            )
        )

    def find_by_name(database, name):
        """Find a jedec 4 bondwire definition by name.

        Parameters
        ----------
        database: Database,
        name: str

        Returns
        -------
        Jedec4BondwireDef
        """
        return Jedec4BondwireDef(
            get_jedec4_bondwire_def_stub().FindByName(
                _QueryBuilder.bondwire_def_str_message(database, name)
            )
        )

    def get_parameters(self):
        """Get parameters of a jedec 4 bondwire definition.

        Returns
        -------
        Value
        """
        return Value(get_jedec4_bondwire_def_stub().GetParameters(self.msg))

    def set_parameters(self, parameter):
        """Set parameters of a jedec 4 bondwire definition.

        Parameters
        ----------
        parameter: Value
        """
        get_jedec4_bondwire_def_stub().SetParameters(
            _Jedec4QueryBuilder.jedec4_bondwire_def_set_parameters_message(self, parameter)
        )

    @property
    def bondwire_type(self):
        """Return jedec 4 bondwire type.

        Returns
        -------
        BondwireDefType
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
    """Class representing a jedec 4 bondwire definition."""

    @staticmethod
    def create(database, name):
        """Create a jedec 5 bondwire definition.

        Parameters
        ----------
        database: Database,
        name: str

        Returns
        -------
        Jedec5BondwireDef
        """
        return Jedec5BondwireDef(
            get_jedec5_bondwire_def_stub().Create(
                _QueryBuilder.bondwire_def_str_message(database, name)
            )
        )

    def find_by_name(database, name):
        """Find a jedec 5 bondwire definition by name.

        Parameters
        ----------
        database: Database,
        name: str

        Returns
        -------
        Jedec5BondwireDef
        """
        return Jedec5BondwireDef(
            get_jedec5_bondwire_def_stub().FindByName(
                _QueryBuilder.bondwire_def_str_message(database, name)
            )
        )

    def get_parameters(self):
        """Get parameters of a jedec 5 bondwire definition.

        Returns
        -------
        Tuple[Value, Value, Value]
        """
        get_parameters_msg = get_jedec5_bondwire_def_stub().GetParameters(self.msg)
        return (
            Value(get_parameters_msg.top_to_die_distance),
            Value(get_parameters_msg.die_pad_angle),
            Value(get_parameters_msg.lead_pad_angle),
        )

    def set_parameters(self, ttd, dpa, lpa):
        """Set parameters of a jedec 5 bondwire definition.

        Parameters
        ----------
        ttd: Value
            Value for top to die distance parameter
        dpa: Value
            Value for die pad angle parameter
        lpa: Value
            Value for lead pad angle parameter
        """
        get_jedec5_bondwire_def_stub().SetParameters(
            _Jedec5QueryBuilder.jedec5_bondwire_def_set_parameters_message(self, ttd, dpa, lpa)
        )

    @property
    def get_bondwire_type(self):
        """Return jedec 5 bondwire type.

        Returns
        -------
        BondwireDefType
        """
        return BondwireDefType.JEDEC5_BONDWIRE_DEF
