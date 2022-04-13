"""This package contains utility functions available to other packages."""

import logging

from .edb_logging import EDBLogger

LOGGER = EDBLogger(level=logging.DEBUG, to_file=False, to_stdout=True)
