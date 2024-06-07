"""RaptorX simulation setup."""

from ansys.edb.core.simulation_setup.raptor_x_simulation_settings import RaptorXSimulationSettings
from ansys.edb.core.simulation_setup.simulation_setup import SimulationSetup, SimulationSetupType


class RaptorXSimulationSetup(SimulationSetup):
    """Represents RaptorX simulation setup data."""

    @classmethod
    def create(cls, cell, name):
        """Create a RaptorX simulation setup.

        Parameters
        ----------
        cell : :class:`.Cell`
            Cell to create the simulation setup in.
        name : str
            Name of the simulation setup.

        Returns
        -------
        RaptorXSimulationSetup
            RaptorX simulation setup created.
        """
        return super()._create(cell, name, SimulationSetupType.RAPTOR_X)

    @property
    def settings(self):
        """:class:`.RaptorXSimulationSettings`: Simulation settings of the RaptorX simulation setup."""
        return RaptorXSimulationSettings(self)
