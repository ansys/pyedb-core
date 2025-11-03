"""SIwavePSI simulation setup."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ansys.edb.core.simulation_setup.simulation_setup import SimulationSetup, SimulationSetupType
from ansys.edb.core.simulation_setup.siwave_psi_simulation_settings import (
    SIwavePSISimulationSettings,
)

if TYPE_CHECKING:
    from ansys.edb.core.layout.cell import Cell


class SIwavePSISimulationSetup(SimulationSetup):
    """Represents SIwavePSI simulation setup data."""

    @classmethod
    def create(cls, cell: Cell, name: str) -> SIwavePSISimulationSetup:
        """Create a SIwavePSI simulation setup.

        Parameters
        ----------
        cell : :class:`.Cell`
            Cell to create the simulation setup in.
        name : str
            Name of the simulation setup.

        Returns
        -------
        SIwavePSISimulationSetup
            SIwavePSI simulation setup created.
        """
        return super()._create(cell, name, SimulationSetupType.SI_WAVE_PSI)

    @property
    def settings(self) -> SIwavePSISimulationSettings:
        """:class:`.SIwavePSISimulationSettings`: Simulation settings of the SIwavePSI simulation setup."""
        return SIwavePSISimulationSettings(self)
