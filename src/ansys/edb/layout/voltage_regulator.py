"""Voltage regulator."""
import ansys.api.edb.v1.voltage_regulator_pb2 as vr_pb2

from ansys.edb.core import ConnObj, LayoutObjType, messages
from ansys.edb.primitive import PadstackInstance
from ansys.edb.session import StubAccessor, StubType
from ansys.edb.utility import Value


class _QueryBuilder:
    @staticmethod
    def create(layout, name, active, voltage, lrc, lrp):
        return vr_pb2.VoltageRegulatorMessage(
            layout=layout.msg, name=name, active=active, voltage=voltage, lrc=lrc, lrp=lrp
        )


class VoltageRegulator(ConnObj):
    """Voltage regulator."""

    __stub = StubAccessor(StubType.voltage_regulator)
    layout_obj_type = LayoutObjType.VOLTAGE_REGULATOR

    @classmethod
    def create(cls, layout, name, active, voltage, lrc, lrp):
        """
        Create voltage regulator class.

        Parameters
        ----------
        layout : Layout
        name : str
        active : bool
        voltage : ValueLike
        lrc : ValueLike
        lrp : ValueLike

        Returns
        -------
        VoltageRegulator
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
        """
        Get name of theVoltage Regulator class.

        Returns
        -------
        str
        """
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, newname):
        """
        Set name of the Voltage Regulator class.

        Parameters
        ----------
        newname : str

        """
        return self.__stub.SetName(messages.edb_obj_name_message(self.msg, newname))

    @property
    def active(self):
        """
        Get active status of the Voltage Regulator class.

        Returns
        -------
        bool
        """
        return self.__stub.IsActive(self.msg).value

    @active.setter
    def active(self, newactive):
        """
        Set active status of the Voltage Regulator class.

        Parameters
        ----------
        newactive : bool

        """
        return self.__stub.SetIsActive(messages.bool_property_message(self, newactive))

    @property
    def voltage(self):
        """
        Get voltage of the Voltage Regulator class.

        Returns
        -------
        Value
        """
        return Value(self.__stub.GetVoltage(self.msg))

    @voltage.setter
    def voltage(self, newvoltage):
        """
        Set name of the Voltage Regulator class.

        Parameters
        ----------
        newvoltage : ValueLike

        """
        return self.__stub.SetVoltage(
            messages.value_property_message(self.msg, messages.value_message(newvoltage))
        )

    @property
    def lrc(self):
        """
        Get load regulation current of the Voltage Regulator class.

        Returns
        -------
        Value
        """
        return Value(self.__stub.GetLoadRegulationCurrent(self.msg))

    @lrc.setter
    def lrc(self, newlrc):
        """
        Set load regulation current of the Voltage Regulator class.

        Parameters
        ----------
        newlrc : ValueLike

        """
        return self.__stub.SetLoadRegulationCurrent(
            messages.value_property_message(self.msg, messages.value_message(newlrc))
        )

    @property
    def lrp(self):
        """
        Get load regulation percent of the Voltage Regulator class.

        Returns
        -------
        Value
        """
        return Value(self.__stub.GetLoadRegulationPercent(self.msg))

    @lrp.setter
    def lrp(self, newlrp):
        """
        Set load regulation percent of the Voltage Regulator class.

        Parameters
        ----------
        newlrp : ValueLike

        """
        return self.__stub.SetLoadRegulationPercent(
            messages.value_property_message(self.msg, messages.value_message(newlrp))
        )

    @property
    def pos_remote_sense_pin(self):
        """
        Get positive remote sense pin of the Voltage Regulator class.

        Returns
        -------
        PadstackInstance
        """
        return PadstackInstance(self.__stub.GetPosRemoteSensePin(self.msg))

    @pos_remote_sense_pin.setter
    def pos_remote_sense_pin(self, newpin):
        """
        Set positive remote sense pin of Voltage Regulator class.

        Parameters
        ----------
        newpin : PadstackInstance

        """
        return self.__stub.SetPosRemoteSensePin(messages.edb_obj_collection_message([self, newpin]))

    @property
    def neg_remote_sense_pin(self):
        """
        Get negative remote sense pin of the Voltage Regulator class.

        Returns
        -------
        PadstackInstance
        """
        return PadstackInstance(self.__stub.GetNegRemoteSensePin(self.msg))

    @neg_remote_sense_pin.setter
    def neg_remote_sense_pin(self, newpin):
        """
        Set negative remote sense pin of Voltage Regulator class.

        Parameters
        ----------
        newpin : PadstackInstance

        """
        return self.__stub.SetNegRemoteSensePin(messages.edb_obj_collection_message([self, newpin]))
