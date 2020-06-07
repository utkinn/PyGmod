"""Configuration script for :mod:`logging` module."""

import sys
import logging

FILE_LEVEL = logging.DEBUG
GMOD_CONSOLE_LEVEL = logging.INFO


class StdoutFilter(logging.Filter):
    """Allows to emit only messages with the severity less than ``ERROR``."""

    # pylint: disable=too-few-public-methods

    def filter(self, record):
        return record.levelno < logging.ERROR


def configure():
    """Configures the :mod:`logging` module.

    All messages with severity at least
    :data:`GMOD_CONSOLE_LEVEL` are configured
    to be printed to the Garry's Mod console.
    All messages with severity at least
    :data:`FILE_LEVEL` are configured
    to be written to ``pygmod.log`` at Garry's Mod root directory.
    """

    pygmod_logger = logging.getLogger("pygmod")
    pygmod_logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("pygmod.log")
    file_handler.setLevel(FILE_LEVEL)
    file_handler.setFormatter(logging.Formatter("[%(name)s|%(levelname)s] %(message)s"))
    pygmod_logger.addHandler(file_handler)

    gmod_console_formatter = logging.Formatter("[PyGmod|%(name)s|%(levelname)s] %(message)s")

    gmod_console_stderr_handler = logging.StreamHandler()
    gmod_console_stderr_handler.setLevel(max(GMOD_CONSOLE_LEVEL, logging.ERROR))
    gmod_console_stderr_handler.setFormatter(gmod_console_formatter)
    pygmod_logger.addHandler(gmod_console_stderr_handler)

    gmod_console_stdout_handler = logging.StreamHandler(sys.stdout)
    gmod_console_stdout_handler.setLevel(GMOD_CONSOLE_LEVEL)
    gmod_console_stdout_handler.addFilter(StdoutFilter())
    gmod_console_stdout_handler.setFormatter(gmod_console_formatter)
    pygmod_logger.addHandler(gmod_console_stdout_handler)

    logging.getLogger("pygmod._logging_config").debug("Logging levels configured")


def test():
    """Function for testing the configuration."""
    logger = logging.getLogger("pygmod")
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")

    logger = logging.getLogger("pygmod.child_logger_test")
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
