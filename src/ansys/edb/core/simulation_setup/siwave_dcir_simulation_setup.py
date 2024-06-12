"""SIWave simulation setup."""

from ansys.edb.core.simulation_setup.simulation_setup import SimulationSetup, SimulationSetupType
from ansys.edb.core.simulation_setup.siwave_dcir_simulation_settings import (
    SIWaveDCIRSimulationSettings,
)


class SIWaveDCIRSimulationSetup(SimulationSetup):
    """Represents SIWave DCIR simulation setup data."""

    @classmethod
    def create(cls, cell, name):
        """Create a SIWave DCIR simulation setup.

        Parameters
        ----------
        cell : :class:`.Cell`
            Cell to create the simulation setup in.
        name : str
            Name of the simulation setup.

        Returns
        -------
        SIWaveDCIRSimulationSetup
            Simulation setup created.
        """
        return super()._create(cell, name, SimulationSetupType.SI_WAVE_DCIR)

    @property
    def settings(self):
        """:class:`.SIWaveSimulationSettings`: Simulation settings of the simulation setup."""
        return SIWaveDCIRSimulationSettings(self)
