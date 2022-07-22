"""Voltage regulator."""
from ansys.edb.core.core import ConnObj, LayoutObjType


class VoltageRegulator(ConnObj):
    """Voltage regulator."""

    layout_type = LayoutObjType.VOLTAGE_REGULATOR

    pass
