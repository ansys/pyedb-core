"""This package contains utility functions available to other packages."""

import logging

from ansys.edb.core.utility.edb_logging import EDBLogger
from ansys.edb.core.utility.value import Value

LOGGER = EDBLogger(level=logging.DEBUG, to_file=False, to_stdout=True)
