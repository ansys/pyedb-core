"""This package contains code unavailable to API users."""

import logging

from ansys.edb.core.core.edb_logging import EDBLogger

LOGGER = EDBLogger(level=logging.DEBUG, to_file=False, to_stdout=True)

from ansys.edb.core.core.base import ObjBase, TypeField
from ansys.edb.core.core.edb_errors import handle_grpc_exception
