"""Temperature Settings."""
from ansys.edb.utility.value import Value


class TemperatureSettings:
    """
    Temperature settings class.

    Attributes
    ----------
    include_temp_dependence : bool
    enable_thermal_feedback : bool
    temperature : :term:`ValueLike`
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
