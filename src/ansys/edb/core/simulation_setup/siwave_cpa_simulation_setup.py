"""SIWave simulation setup."""

from ansys.edb.core.simulation_setup.simulation_setup import SimulationSetup
from ansys.edb.core.simulation_setup.simulation_setup import SimulationSetupType
from ansys.edb.core.simulation_setup.siwave_cpa_simulation_settings import SIWaveCPASimulationSettings


class SIWaveCPASimulationSetup(SimulationSetup):
    """Represents SIWave CPA simulation setup data."""

    @classmethod
    def create(cls, cell, name):
        """Create a SIWave CPA simulation setup.

        Parameters
        ----------
        cell : :class:`.Cell`
            Cell to create the simulation setup in.
        name : str
            Name of the simulation setup.

        Returns
        -------
        SIWaveCPASimulationSetup
            Simulation setup created.
        """
        return super()._create(cell, name, SimulationSetupType.SI_WAVE_CPA)

    @property
    def settings(self):
        """:class:`.SIWaveCPASimulationSettings`: Simulation settings of the simulation setup."""
        return SIWaveCPASimulationSettings(self)
