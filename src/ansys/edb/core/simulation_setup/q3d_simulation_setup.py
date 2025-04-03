"""Q3D simulation setup."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ansys.edb.core.simulation_setup.q3d_simulation_settings import Q3DSimulationSettings
from ansys.edb.core.simulation_setup.simulation_setup import SimulationSetup, SimulationSetupType

if TYPE_CHECKING:
    from ansys.edb.core.layout.cell import Cell


class Q3DSimulationSetup(SimulationSetup):
    """Represents Q3D simulation setup data."""

    @classmethod
    def create(cls, cell: Cell, name: str) -> Q3DSimulationSetup:
        """Create a Q3D simulation setup.

        Parameters
        ----------
        cell : :class:`.Cell`
            Cell to create the simulation setup in.
        name : str
            Name of the simulation setup.

        Returns
        -------
        Q3DSimulationSetup
            Q3D simulation setup created.
        """
        return super()._create(cell, name, SimulationSetupType.Q3D_SIM)

    @property
    def settings(self) -> Q3DSimulationSettings:
        """:class:`.Q3DSimulationSettings`: Simulation settings of the Q3D simulation setup."""
        return Q3DSimulationSettings(self)
