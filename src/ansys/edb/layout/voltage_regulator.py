"""Voltage regulator."""
import ansys.api.edb.v1.voltage_regulator_pb2 as vr_pb2

from ansys.edb.core import conn_obj, messages
from ansys.edb.edb_defs import LayoutObjType
from ansys.edb.primitive import PadstackInstance
from ansys.edb.session import StubAccessor, StubType
from ansys.edb.utility import Value


class _QueryBuilder:
    @staticmethod
    def create(layout, name, active, voltage, lrc, lrp):
        return vr_pb2.VoltageRegulatorMessage(
            layout=layout.msg, name=name, active=active, voltage=voltage, lrc=lrc, lrp=lrp
        )


class VoltageRegulator(conn_obj.ConnObj):
    """Voltage regulator."""

    __stub = StubAccessor(StubType.voltage_regulator)
    layout_obj_type = LayoutObjType.VOLTAGE_REGULATOR

    @classmethod
    def create(cls, layout, name, active, voltage, lrc, lrp):
        """
        Create a voltage regulator.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout the voltage regulator will be in.
        name : str
            The name of the voltage regulator.
        active : bool
            The voltage regulators active state.
        voltage : :term:`ValueLike`
            The voltage of the VoltageRegulator
        lrc : :term:`ValueLike`
            The load regulation current
        lrp : :term:`ValueLike`
            The load regulation percent.

        Returns
        -------
        VoltageRegulator
            Newly created voltage regulator.
        """
        return VoltageRegulator(
            cls.__stub.Create(
                _QueryBuilder.create(
                    layout,
                    name,
                    active,
                    messages.value_message(voltage),
                    messages.value_message(lrc),
                    messages.value_message(lrp),
                )
            )
        )

    @property
    def name(self):
        """:obj:`str`: Name of the voltage regulator."""
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, newname):
        self.__stub.SetName(messages.edb_obj_name_message(self.msg, newname))

    @property
    def active(self):
        """:obj:`bool`: Active status of the Voltage Regulator."""
        return self.__stub.IsActive(self.msg).value

    @active.setter
    def active(self, newactive):
        self.__stub.SetIsActive(messages.bool_property_message(self, newactive))

    @property
    def voltage(self):
        """:class:`Value <ansys.edb.utility.Value>`: Voltage of the Voltage Regulator.

        Property can be set with :term:`ValueLike`
        """
        return Value(self.__stub.GetVoltage(self.msg))

    @voltage.setter
    def voltage(self, newvoltage):
        self.__stub.SetVoltage(
            messages.value_property_message(self.msg, messages.value_message(newvoltage))
        )

    @property
    def lrc(self):
        """:class:`Value <ansys.edb.utility.Value>`: Load regulation current of the Voltage Regulator.

        Property can be set with :term:`ValueLike`
        """
        return Value(self.__stub.GetLoadRegulationCurrent(self.msg))

    @lrc.setter
    def lrc(self, newlrc):
        self.__stub.SetLoadRegulationCurrent(
            messages.value_property_message(self.msg, messages.value_message(newlrc))
        )

    @property
    def lrp(self):
        """:class:`Value <ansys.edb.utility.Value>`: Load regulation percent of the Voltage Regulator.

        Property can be set with :term:`ValueLike`
        """
        return Value(self.__stub.GetLoadRegulationPercent(self.msg))

    @lrp.setter
    def lrp(self, newlrp):
        self.__stub.SetLoadRegulationPercent(
            messages.value_property_message(self.msg, messages.value_message(newlrp))
        )

    @property
    def pos_remote_sense_pin(self):
        """:class:`PadstackInstance <ansys.edb.primitive.PadstackInstance>`: Positive remote sense pin of the \
        Voltage Regulator.

        .. seealso:: :obj:`neg_remote_sense_pin`
        """
        return PadstackInstance(self.__stub.GetPosRemoteSensePin(self.msg))

    @pos_remote_sense_pin.setter
    def pos_remote_sense_pin(self, newpin):
        self.__stub.SetPosRemoteSensePin(messages.edb_obj_collection_message([self, newpin]))

    @property
    def neg_remote_sense_pin(self):
        """:class:`PadstackInstance <ansys.edb.primitive.PadstackInstance>`: Negative remote sense pin of the \
        Voltage Regulator.

        .. seealso:: :obj:`pos_remote_sense_pin`
        """
        return PadstackInstance(self.__stub.GetNegRemoteSensePin(self.msg))

    @neg_remote_sense_pin.setter
    def neg_remote_sense_pin(self, newpin):
        self.__stub.SetNegRemoteSensePin(messages.edb_obj_collection_message([self, newpin]))
