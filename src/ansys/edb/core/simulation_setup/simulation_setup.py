"""Simulation Setup."""

from enum import Enum

from ansys.api.edb.v1 import edb_defs_pb2
from ansys.api.edb.v1.simulation_setup_pb2 import (
    SimulationSetupCreationMessage,
    SweepDataListMessage,
    SweepDataListPropertyMessage,
    SweepDataMessage,
)

from ansys.edb.core.inner import messages
from ansys.edb.core.inner.base import ObjBase
from ansys.edb.core.session import SimulationSetupServiceStub, StubAccessor, StubType


class SimulationSetupType(Enum):
    """Enum representing available simulation setup types."""

    HFSS = edb_defs_pb2.HFSS_SIM
    SI_WAVE = edb_defs_pb2.SI_WAVE_SIM
    SI_WAVE_DCIR = edb_defs_pb2.SI_WAVE_DCIR_SIM
    RAPTOR_X = edb_defs_pb2.RAPTOR_X_SIM


class SweepData:
    r"""Class representing a sweep data setting.

    Attributes
    ----------
    name : str
      Name of this sweep.
    distribution : str
      Type of sweep (see table below).
    start_f : str
      Start frequency is number with optional frequency units.
    end_f : str
      End frequency is number with optional frequency units.
    step : str
      Step is either frequency with optional frequency units or an integer when a count is needed.
    fast_sweep : bool, default: False
      Whether this is a fast sweep.

    Notes
    -----
    Here are the choices for the distribution parameter:

    .. list-table:: Values for distribution parameter
       :widths: 20 45 25
       :header-rows: 1

       * - Distribution
         - Description
         - Example
       * - LIN
         - linear (start, stop, step)
         - LIN 2GHz 4GHz 100MHz or LIN 1dBm 10dBm 1dB
       * - LINC
         - linear (start, stop, count)
         - LINC 2GHz 4GHz 11
       * - ESTP
         - Exponential step (start, stop, count)
         - ESTP 2MHz 10MHz 3
       * - DEC
         - decade (start, stop, number of decades)
         - DEC 10KHz 10GHz 6
       * - OCT
         - octave (start, stop, number of octaves)
         - OCT 10MHz 160MHz 5

    """

    def __init__(
        self,
        name,
        distribution,
        start_f,
        end_f,
        step,
        fast_sweep=False,
    ):
        """Initialize a sweep data setting."""
        self.name = name
        self.distribution = distribution
        self.start_f = start_f
        self.end_f = end_f
        self.step = step
        self.fast_sweep = fast_sweep

    @property
    def frequency_string(self):
        """:obj:`str`: String representing the frequency sweep data."""
        return self.distribution + " " + self.start_f + " " + self.end_f + " " + self.step


class SimulationSetup(ObjBase):
    """Class representing base simulation setup data."""

    __stub: SimulationSetupServiceStub = StubAccessor(StubType.sim_setup)

    @classmethod
    def _create(cls, cell, sim_setup_name, sim_setup_type):
        return cls(
            SimulationSetup.__stub.Create(
                SimulationSetupCreationMessage(
                    cell=cell.msg, name=sim_setup_name, type=sim_setup_type.value
                )
            )
        )

    @property
    def name(self):
        """:obj:`str`: Name of simulation setup."""
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, name):
        self.__stub.SetName(messages.string_property_message(self, name))

    @property
    def position(self):
        """:obj:`int`: Position of the simulation in the setup order."""
        return self.__stub.GetPosition(self.msg).value

    @position.setter
    def position(self, position):
        self.__stub.SetPosition(messages.int_property_message(self, position))

    @property
    def sweep_data(self):
        """:obj:`list` of :class:`SweepData`: Frequency sweeps of the simulation setup."""
        sweep_data = []
        for sweep_data_msg in self.__stub.GetSweepData(self.msg).sweep_data:
            freq_str_params = sweep_data_msg.frequency_string.split()
            new_sweep_data = SweepData(
                sweep_data_msg.name,
                freq_str_params[0],
                freq_str_params[1],
                freq_str_params[2],
                freq_str_params[3],
                sweep_data_msg.fast_sweep,
            )
            sweep_data.append(new_sweep_data)
        return sweep_data

    @sweep_data.setter
    def sweep_data(self, sweep_data):
        sweep_data_msgs = []
        for sweep in sweep_data:
            sweep_data_msgs.append(
                SweepDataMessage(
                    name=sweep.name,
                    frequency_string=sweep.frequency_string,
                    fast_sweep=sweep.fast_sweep,
                )
            )
        self.__stub.SetSweepData(
            SweepDataListPropertyMessage(
                target=self.msg, sweeps=SweepDataListMessage(sweep_data=sweep_data_msgs)
            )
        )

    @property
    def type(self):
        """:class:`SimulationSetupType`: Type of the simulation setup."""
        return SimulationSetupType(self.__stub.GetType(self.msg).type)

    def cast(self):
        """Cast the base SimulationSetup object to correct subclass, if possible.

        Returns
        -------
        SimulationSetup
        """
        from ansys.edb.core.simulation_setup import (
            HfssSimulationSetup,
            RaptorXSimulationSetup,
            SIWaveDCIRSimulationSetup,
            SIWaveSimulationSetup,
        )

        if self.is_null:
            return

        sim_type = self.type
        if sim_type == SimulationSetupType.HFSS:
            return HfssSimulationSetup(self.msg)
        elif sim_type == SimulationSetupType.SI_WAVE:
            return SIWaveSimulationSetup(self.msg)
        elif sim_type == SimulationSetupType.SI_WAVE_DCIR:
            return SIWaveDCIRSimulationSetup(self.msg)
        elif sim_type == SimulationSetupType.RAPTOR_X:
            return RaptorXSimulationSetup(self.msg)
