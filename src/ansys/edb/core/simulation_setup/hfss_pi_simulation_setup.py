# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""HFSSPI simulation setup."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ansys.edb.core.simulation_setup.hfss_pi_simulation_settings import HFSSPISimulationSettings
from ansys.edb.core.simulation_setup.simulation_setup import SimulationSetup
from ansys.edb.core.simulation_setup.simulation_setup import SimulationSetupType

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
