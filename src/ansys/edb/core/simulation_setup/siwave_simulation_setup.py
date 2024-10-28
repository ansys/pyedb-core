# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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

"""SIWave simulation setup."""

from ansys.edb.core.simulation_setup.simulation_setup import SimulationSetup, SimulationSetupType
from ansys.edb.core.simulation_setup.siwave_simulation_settings import SIWaveSimulationSettings


class SIWaveSimulationSetup(SimulationSetup):
    """Represents SIWave simulation setup data."""

    @classmethod
    def create(cls, cell, name):
        """Create a SIWave simulationsetup.

        Parameters
        ----------
        cell : :class:`.Cell`
            Cell to create simulation setup in.
        name : str
            Name of the simulation setup.

        Returns
        -------
        SIWaveSimulationSetup
            Simulation setup created.
        """
        return super()._create(cell, name, SimulationSetupType.SI_WAVE)

    @property
    def settings(self):
        """:class:`.SIWaveSimulationSettings`: Simulation settings of the SIWave simulation setup."""
        return SIWaveSimulationSettings(self)
