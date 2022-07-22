"""Extended Net."""

from ansys.edb.core.core import LayoutObjType
from ansys.edb.core.net.net_class import NetClass


class ExtendedNet(NetClass):
    """Extended net class."""

    layout_type = LayoutObjType.EXTENDED_NET

    pass
