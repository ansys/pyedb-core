"""This package contains code unavailable to API users."""

import logging

from ansys.edb.core.inner.base import ObjBase, TypeField
from ansys.edb.core.inner.edb_logging import EDBLogger

LOGGER = EDBLogger(level=logging.DEBUG, to_file=False, to_stdout=True)
