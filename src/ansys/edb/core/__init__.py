"""This package contains code unavailable to API users."""

import logging

from ansys.edb.core.base import ObjBase, TypeField
from ansys.edb.core.conn_obj import ConnObj
from ansys.edb.core.edb_logging import EDBLogger
from ansys.edb.core.layout_obj import LayoutObj, LayoutObjType
from ansys.edb.core.variable_server import VariableServer

LOGGER = EDBLogger(level=logging.DEBUG, to_file=False, to_stdout=True)
