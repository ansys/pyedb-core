"""Extended Net."""

from ansys.edb.core import LayoutObjType
from ansys.edb.net.net_class import NetClass


class ExtendedNet(NetClass):
    """Extended net class."""

    layout_obj_type = LayoutObjType.EXTENDED_NET

    pass
