"""SIWave Simulation Setup."""

from ansys.edb.simulation_setup.simulation_setup import SimulationSetup, SimulationSetupType
from ansys.edb.simulation_setup.siwave_dcir_simulation_settings import SIWaveDCIRSimulationSettings


class SIWaveDCIRSimulationSetup(SimulationSetup):
    """Class representing SIWave DCIR simulation setup data."""

    @classmethod
    def create(cls, cell, name):
        """Create a SIWaveDCIRSimulationSetup.

        Parameters
        ----------
        cell : :class:`Cell <ansys.edb.layout.Cell>`
            Cell containing new simulation setup.
        name : str
            Name of new simulation setup

        Returns
        -------
        SIWaveDCIRSimulationSetup
            Newly created simulation setup.
        """
        return super()._create(cell, name, SimulationSetupType.SI_WAVE_DCIR)

    @property
    def settings(self):
        """:class:`SIWaveSimulationSettings`: Simulation settings of the siwave simulation setup."""
        return SIWaveDCIRSimulationSettings(self)
