"""RaptorX Simulation Setup."""

from ansys.edb.core.simulation_setup.raptor_x_simulation_settings import RaptorXSimulationSettings
from ansys.edb.core.simulation_setup.simulation_setup import SimulationSetup, SimulationSetupType


class RaptorXSimulationSetup(SimulationSetup):
    """Class representing RaptorX simulation setup data."""

    @classmethod
    def create(cls, cell, name):
        """Create a RaptorXSimulationSetup.

        Parameters
        ----------
        cell : :class:`Cell <ansys.edb.core.layout.Cell>`
            Cell containing new simulation setup.
        name : str
            Name of new simulation setup

        Returns
        -------
        RaptorXSimulationSetup
            Newly created simulation setup.
        """
        return super()._create(cell, name, SimulationSetupType.RAPTOR_X)

    @property
    def settings(self):
        """:class:`RaptorXSimulationSettings`: Simulation settings of the RaptorX simulation setup."""
        return RaptorXSimulationSettings(self)
