"""Extended Net."""

from ansys.edb.edb_defs import LayoutObjType
from ansys.edb.net import net_class


class ExtendedNet(net_class.NetClass):
    """Extended net class."""

    layout_obj_type = LayoutObjType.EXTENDED_NET

    pass
