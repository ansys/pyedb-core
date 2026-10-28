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
