"""Voltage regulator."""
from ansys.edb.core.layout.conn_obj import ConnObj
from ansys.edb.core.layout.layout_obj import LayoutObjType


class VoltageRegulator(ConnObj):
    """Voltage regulator."""

    layout_type = LayoutObjType.VOLTAGE_REGULATOR
    pass
