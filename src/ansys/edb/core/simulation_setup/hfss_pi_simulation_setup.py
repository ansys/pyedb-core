"""HFSSPI simulation setup."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ansys.edb.core.simulation_setup.hfss_pi_simulation_settings import HFSSPISimulationSettings
from ansys.edb.core.simulation_setup.simulation_setup import SimulationSetup, SimulationSetupType

if TYPE_CHECKING:
    from ansys.edb.core.layout.cell import Cell


class HFSSPISimulationSetup(SimulationSetup):
    """Represents HFSSPI simulation setup data."""

    @classmethod
    def create(cls, cell: Cell, name: str) -> HFSSPISimulationSetup:
        """Create a HFSSPI simulation setup.

        Parameters
        ----------
        cell : :class:`.Cell`
            Cell to create the simulation setup in.
        name : str
            Name of the simulation setup.

        Returns
        -------
        HFSSPISimulationSetup
            HFSSPI simulation setup created.
        """
        return super()._create(cell, name, SimulationSetupType.HFSS_PI)

    @property
    def settings(self) -> HFSSPISimulationSettings:
        """:class:`.HFSSPISimulationSettings`: Simulation settings of the HFSSPI simulation setup."""
        return HFSSPISimulationSettings(self)
