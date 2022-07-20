"""Differential pair."""
from ansys.edb.core.layout.layout_obj import LayoutObjType
from ansys.edb.core.net.net_class import NetClass


class DifferentialPair(NetClass):
    """Differential pair class."""

    layout_type = LayoutObjType.DIFFERENTIAL_PAIR
    pass
