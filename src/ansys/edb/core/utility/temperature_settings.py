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

"""Temperature settings."""
from ansys.edb.core.utility.value import Value


class TemperatureSettings:
    """
    Provides temperature settings.

    Attributes
    ----------
    include_temp_dependence : bool
        Whether to include temperature dependence.
    enable_thermal_feedback : bool
        Whether to enable thermal feedback.
    temperature : :term:`ValueLike`
        Temperature value.
    """

    def __init__(self, include_temp_dependence, enable_thermal_feedback, temperature):
        """Initialize temperature settings."""
        self.include_temp_dependence = include_temp_dependence
        self.enable_thermal_feedback = enable_thermal_feedback
        self.temperature = temperature

    def __eq__(self, other):
        """Compare equality with another object."""
        if isinstance(other, TemperatureSettings):
            return (
                self.include_temp_dependence == other.include_temp_dependence
                and self.enable_thermal_feedback == other.enable_thermal_feedback
                and Value(self.temperature) == Value(other.temperature)
            )
        return False
