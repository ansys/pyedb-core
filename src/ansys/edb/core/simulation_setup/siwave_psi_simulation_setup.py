"""SIWavePSI simulation setup."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ansys.edb.core.simulation_setup.simulation_setup import SimulationSetup, SimulationSetupType
from ansys.edb.core.simulation_setup.siwave_psi_simulation_settings import (
    SIWavePSISimulationSettings,
)

if TYPE_CHECKING:
    from ansys.edb.core.layout.cell import Cell


class SIWavePSISimulationSetup(SimulationSetup):
    """Represents SIWavePSI simulation setup data."""

    @classmethod
    def create(cls, cell: Cell, name: str) -> SIWavePSISimulationSetup:
        """Create a SIWavePSI simulation setup.

        Parameters
        ----------
        cell : :class:`.Cell`
            Cell to create the simulation setup in.
        name : str
            Name of the simulation setup.

        Returns
        -------
        SIWavePSISimulationSetup
            SIWavePSI simulation setup created.
        """
        return super()._create(cell, name, SimulationSetupType.SI_WAVE_PSI)

    @property
    def settings(self) -> SIWavePSISimulationSettings:
        """:class:`.SIWavePSISimulationSettings`: Simulation settings of the SIWavePSI simulation setup."""
        return SIWavePSISimulationSettings(self)
