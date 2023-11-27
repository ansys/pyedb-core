"""``log`` module.

## Objective
This module intends to create a general framework for logging.
This module is built upon ``logging`` library and it does NOT intend to
replace it rather provide a way to interact between ``logging`` and ``EDB Client``.

Usage
-----

Global logger
-------------

There is a global logger named ``EDB_LOGGER`
If you want to use this global logger, you must call at the top of your module:

.. code::
    from ansys.edb.core.utility import EDB_LOG

It should be noticed that the default logging level of ``LOG`` is ``ERROR``.
To change this and output lower level messages you can use the next snippet:

.. code::
   EDB_LOG.setLevel(logging.DEBUG)

By default, this logger does not log to a file.
If you wish to do so, you can add a file handler using:

.. code::
   import os
   file_path = os.path.join(os.getcwd(), 'edb_client.log')
   EDB_LOG.log_to_file(file_path)

This sets the logger to be redirected also to that file.

To log using this logger, just call the desired method as a normal logger.

.. code::
    import logging
    from ansys.edb.core.utility import edb_logging
    LOGGER = EDBLogger(level=logging.DEBUG, to_file=False, to_stdout=True)
    LOGGER.debug('This is LOG debug message.')

    | DEBUG    | This is LOG debug message.
"""

from datetime import datetime
import logging
import sys

# Default configuration
LOG_LEVEL = logging.DEBUG
FILE_NAME = "edb_client.log"

# Formatting

STDOUT_MSG_FORMAT = "%(levelname)s - %(message)s"

FILE_MSG_FORMAT = STDOUT_MSG_FORMAT

DEFAULT_STDOUT_HEADER = """
"""
DEFAULT_FILE_HEADER = DEFAULT_STDOUT_HEADER

NEW_SESSION_HEADER = f"""
===============================================================================
       NEW SESSION - {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
==============================================================================="""


class EDBLogger:
    """EDBLogger used for each edb_client session.

    This class allows you to add handler to a file or standard output.
    """

    file_handler = None
    std_out_handler = None

    def __init__(self, level=logging.DEBUG, to_file=False, to_stdout=True, filename=FILE_NAME):
        """Customize logger class for edb_client.

        Parameters
        ----------
        level : int, optional
            Level of logging as defined in the package ``logging``. By default 'DEBUG'.
        to_file : bool, optional
            To record the logs in a file, by default ``False``.
        to_stdout : bool, optional
            To output the logs to the standard output, which is the
            command line. By default ``True``.
        filename : str, optional
            Name of the output file. By default ``edb_client.log``.
        """
        self.logger = logging.getLogger("edb_client")  # Creating default main logger.
        self.logger.setLevel(level)
        self.logger.propagate = True

        if to_file or filename != FILE_NAME:
            # We record to file
            self.log_to_file(filename=filename, level=level)

        if to_stdout:
            self.log_to_stdout(level=level)

        add_handling_uncaught_exceptions(self.logger)  # Using logger to record unhandled exceptions

    def __getattr__(self, item):
        """Delegate method calls to logger."""
        return getattr(self.logger, item)

    def stop_logging_to_stdout(self):
        """Stop logging to stdout."""
        if self.std_out_handler is not None:
            self.logger.removeHandler(self.std_out_handler)
            self.std_out_handler = None

    def stop_logging_to_file(self):
        """Stop logging to file."""
        if self.file_handler is not None:
            self.logger.removeHandler(self.file_handler)
            self.file_handler = None

    def log_to_file(self, filename=FILE_NAME, level=LOG_LEVEL):
        """Add file handler to logger.

        Parameters
        ----------
        filename : str, optional
            Name of the file where the logs are recorded. By default FILE_NAME
        level : str, optional
            Level of logging. E.x. 'DEBUG'. By default LOG_LEVEL
        """
        addfile_handler(self, filename=filename, level=level, write_headers=True)

    def log_to_stdout(self, level=LOG_LEVEL):
        """Add standard output handler to the logger.

        Parameters
        ----------
        level : str, optional
            Level of logging record. By default LOG_LEVEL
        """
        add_stdout_handler(self, level=level)


# Auxiliary functions


def add_handling_uncaught_exceptions(logger):
    """Redirects the output of an exception to the logger."""

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception


def addfile_handler(edb_logger, filename=FILE_NAME, level=LOG_LEVEL, write_headers=False):
    """
    Add a file handler to the input.

    Parameters
    ----------
    edb_logger : EDBLogger
        EDBLogger where to add the file handler.
    filename : str, optional
        Name of the output file. By default FILE_NAME
    level : str, optional
        Level of log recording. By default LOG_LEVEL
    write_headers : bool, optional
        Record the headers to the file. By default False

    Returns
    -------
    logger
        Return the EDBLogger object.
    """
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(FILE_MSG_FORMAT))

    if isinstance(edb_logger, EDBLogger):
        edb_logger.file_handler = file_handler
        edb_logger.logger.addHandler(file_handler)

    if write_headers:
        file_handler.stream.write(NEW_SESSION_HEADER)
        file_handler.stream.write(DEFAULT_FILE_HEADER)

    return edb_logger


def add_stdout_handler(edb_logger, level=LOG_LEVEL, write_headers=False):
    """Add a file handler to the logger.

    Parameters
    ----------
    edb_logger : EDBLogger
        EDBLogger where to add the file handler.
    level : str, optional
        Level of log recording. By default ``logging.DEBUG``.
    write_headers : bool, optional
        Record the headers to the file. By default ``False``.

    Returns
    -------
    logger
        The EDBLogger object.
    """
    std_out_handler = logging.StreamHandler()
    std_out_handler.setLevel(level)
    std_out_handler.setFormatter(logging.Formatter(STDOUT_MSG_FORMAT))

    if isinstance(edb_logger, EDBLogger):
        edb_logger.std_out_handler = std_out_handler
        edb_logger.logger.addHandler(std_out_handler)

    if write_headers:
        std_out_handler.stream.write(DEFAULT_STDOUT_HEADER)

    return edb_logger
