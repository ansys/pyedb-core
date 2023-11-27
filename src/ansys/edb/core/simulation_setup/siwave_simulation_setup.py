"""SIWave Simulation Setup."""

from ansys.edb.core.simulation_setup.simulation_setup import SimulationSetup, SimulationSetupType
from ansys.edb.core.simulation_setup.siwave_simulation_settings import SIWaveSimulationSettings


class SIWaveSimulationSetup(SimulationSetup):
    """Class representing SIWave simulation setup data."""

    @classmethod
    def create(cls, cell, name):
        """Create a SIWaveSimulationSetup.

        Parameters
        ----------
        cell : :class:`Cell <ansys.edb.core.layout.Cell>`
            Cell containing new simulation setup.
        name : str
            Name of new simulation setup

        Returns
        -------
        SIWaveSimulationSetup
            Newly created simulation setup.
        """
        return super()._create(cell, name, SimulationSetupType.SI_WAVE)

    @property
    def settings(self):
        """:class:`SIWaveSimulationSettings`: Simulation settings of the SIWave simulation setup."""
        return SIWaveSimulationSettings(self)
