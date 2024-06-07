"""SIWave simulation setup."""

from ansys.edb.core.simulation_setup.simulation_setup import SimulationSetup, SimulationSetupType
from ansys.edb.core.simulation_setup.siwave_simulation_settings import SIWaveSimulationSettings


class SIWaveSimulationSetup(SimulationSetup):
    """Represents SIWave simulation setup data."""

    @classmethod
    def create(cls, cell, name):
        """Create a SIWave simulationsetup.

        Parameters
        ----------
        cell : :class:`.Cell`
            Cell to create simulation setup in.
        name : str
            Name of the simulation setup.

        Returns
        -------
        SIWaveSimulationSetup
            Simulation setup created.
        """
        return super()._create(cell, name, SimulationSetupType.SI_WAVE)

    @property
    def settings(self):
        """:class:`.SIWaveSimulationSettings`: Simulation settings of the SIWave simulation setup."""
        return SIWaveSimulationSettings(self)
