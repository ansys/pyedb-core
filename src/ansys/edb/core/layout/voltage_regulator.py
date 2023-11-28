"""Voltage regulator."""
import ansys.api.edb.v1.voltage_regulator_pb2 as vr_pb2

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.inner import conn_obj, messages
from ansys.edb.core.primitive import PadstackInstance
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility import Value


class PowerModule:
    """Class representing a Power Module.

    Attributes
    ----------
    comp_group_name : str
        Component Group Name.
    pos_output_terminal : str
        Name of the Positive Output Terminal.
    neg_output_terminal : str
        Name of the Negative Output Terminal
    relative_strength : :class:`Value <ansys.edb.core.utility.Value>`
        Relative strength in %
    active : bool
        True if active
    """

    def __init__(
        self,
        comp_group_name,
        pos_output_terminal="",
        neg_output_terminal="",
        relative_strength=Value(100),
        active=True,
    ):
        """Construct a Power Module."""
        self._comp_group_name = comp_group_name
        self._pos_output_terminal = pos_output_terminal
        self._neg_output_terminal = neg_output_terminal
        self._relative_strength = Value(relative_strength)
        self._active = active
        self._needs_sync = True

    @property
    def comp_group_name(self):
        """:obj:`str`: Component Group Name of this Power Module."""
        return self._comp_group_name

    @comp_group_name.setter
    def comp_group_name(self, comp_group_name):
        self._comp_group_name = comp_group_name

    @property
    def pos_output_terminal(self):
        """:obj:`str`: Positive Output Terminal name for this Power Module."""
        return self._pos_output_terminal

    @pos_output_terminal.setter
    def pos_output_terminal(self, pos_output_terminal):
        self._pos_output_terminal = pos_output_terminal

    @property
    def neg_output_terminal(self):
        """:obj:`str`: Negative Output Terminal name for this Power Module."""
        return self._neg_output_terminal

    @neg_output_terminal.setter
    def neg_output_terminal(self, neg_output_terminal):
        self._neg_output_terminal = neg_output_terminal

    @property
    def relative_strength(self):
        """:class:`Value <ansys.edb.core.utility.Value>` : Relative Strength for this Power Module in percent.

        Property can be set with :term:`ValueLike`
        """
        return self._relative_strength

    @relative_strength.setter
    def relative_strength(self, relative_strength):
        self._relative_strength = relative_strength

    @property
    def active(self):
        """:obj:`bool`: True if this Power Module is active."""
        return self._active

    @active.setter
    def active(self, active):
        self._active = active

    @property
    def needs_sync(self):
        """:obj:`bool`: True if this Power Module needs to be synchronized.

        Read-Only
        """
        return self._needs_sync


class _QueryBuilder:
    @staticmethod
    def create(layout, name, active, voltage, lrc, lrp):
        return vr_pb2.VoltageRegulatorMessage(
            layout=layout.msg, name=name, active=active, voltage=voltage, lrc=lrc, lrp=lrp
        )

    @staticmethod
    def create_power_module(msg):
        return PowerModule(
            comp_group_name=msg.comp_group_name,
            pos_output_terminal=msg.pos_output_terminal,
            neg_output_terminal=msg.neg_output_terminal,
            relative_strength=msg.relative_strength,
            active=msg.active,
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
        layout : :class:`Layout <ansys.edb.core.layout.Layout>`
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
        """:class:`Value <ansys.edb.core.utility.Value>`: Voltage of the Voltage Regulator.

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
        """:class:`Value <ansys.edb.core.utility.Value>`: Load regulation current of the Voltage Regulator.

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
        """:class:`Value <ansys.edb.core.utility.Value>`: Load regulation percent of the Voltage Regulator.

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
        """:class:`PadstackInstance <ansys.edb.core.primitive.PadstackInstance>`: Positive remote sense pin of the \
        Voltage Regulator.

        .. seealso:: :obj:`neg_remote_sense_pin`
        """
        return PadstackInstance(self.__stub.GetPosRemoteSensePin(self.msg))

    @pos_remote_sense_pin.setter
    def pos_remote_sense_pin(self, newpin):
        self.__stub.SetPosRemoteSensePin(messages.edb_obj_collection_message([self, newpin]))

    @property
    def neg_remote_sense_pin(self):
        """:class:`PadstackInstance <ansys.edb.core.primitive.PadstackInstance>`: Negative remote sense pin of the \
        Voltage Regulator.

        .. seealso:: :obj:`pos_remote_sense_pin`
        """
        return PadstackInstance(self.__stub.GetNegRemoteSensePin(self.msg))

    @neg_remote_sense_pin.setter
    def neg_remote_sense_pin(self, newpin):
        self.__stub.SetNegRemoteSensePin(messages.edb_obj_collection_message([self, newpin]))

    @property
    def num_power_modules(self):
        """:obj: `int` : Number of power modules.

        Read-Only
        """
        return self.__stub.GetNPowerModules(self.msg).value

    @property
    def num_active_power_modules(self):
        """:obj: `int` : Number of active power modules.

        Read-Only
        """
        return self.__stub.GetNActivePowerModules(self.msg).value

    def get_power_module(self, comp_group_name):
        """Get power module corresponding to the component group name.

        Parameters
        ----------
        comp_group_name : str
            Component group name of the power module

        Returns
        -------
        PowerModule
        """
        return _QueryBuilder.create_power_module(
            msg=self.__stub.GetPowerModule(messages.string_property_message(self, comp_group_name))
        )

    def get_all_power_modules(self):
        """Get all power modules in this voltage regulator.

        Returns
        -------
        list[PowerModule]
        """
        all_pms = self.__stub.GetAllPowerModules(self.msg)

        return [_QueryBuilder.create_power_module(msg=msg) for msg in all_pms.data]

    def add_power_module(self, power_module):
        """Add a Power Module to this Voltage Regulator.

        Parameters
        ----------
        power_module : PowerModule
            PowerModule to be added
        """
        self.__stub.AddPowerModule(
            vr_pb2.PowerModulePropertyMessage(
                vrm=self.msg, module=messages.power_module_message(power_module)
            )
        )

    def remove_power_module(self, name):
        """Remove a Power Module from this Voltage Regulator.

        Parameters
        ----------
        name : str
            Component Group Name of the Power Module to be removed.
        """
        self.__stub.RemovePowerModule(messages.string_property_message(target=self, value=name))

    def add_power_modules(self, power_modules):
        """Add multiple Power Modules to this Voltage Regulator.

        Parameters
        ----------
        power_modules : list[PowerModule]
            Power Modules to be added
        """
        self.__stub.AddPowerModules([messages.power_module_message(pm) for pm in power_modules])

    def remove_power_modules(self, names):
        """Remove multiple Power Modules.

        Parameters
        ----------
        names : list[str]
            Component Group Names of each Power Module to remove.

        """
        self.__stub.RemovePowerModules(messages.strings_property_message(target=self, value=names))

    def remove_all_power_modules(self):
        """Remove all Power Modules in this Voltage Regulator."""
        self.__stub.RemoveAllPowerModules(self.msg)
