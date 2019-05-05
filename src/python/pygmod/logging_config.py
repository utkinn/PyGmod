"""Configuration script for :mod:`logging` module."""

import sys
import logging

FILE_LEVEL = logging.DEBUG
GMOD_CONSOLE_LEVEL = logging.INFO


class StdoutFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR


def configure():
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger().handlers.clear()

    pygmod_logger = logging.getLogger("pygmod")

    file_handler = logging.FileHandler("pygmod.log")
    file_handler.setLevel(FILE_LEVEL)
    file_handler.setFormatter(logging.Formatter("[%(name)s|%(levelname)s] %(message)s"))
    pygmod_logger.addHandler(file_handler)

    gmod_console_formatter = logging.Formatter("[PyGmod|%(name)s|%(levelname)s] %(message)s")

    gmod_console_stderr_handler = logging.StreamHandler()
    gmod_console_stderr_handler.setLevel(max(logging.ERROR, GMOD_CONSOLE_LEVEL))
    gmod_console_stderr_handler.setFormatter(gmod_console_formatter)
    pygmod_logger.addHandler(gmod_console_stderr_handler)

    gmod_console_stdout_handler = logging.StreamHandler(sys.stdout)
    gmod_console_stderr_handler.setLevel(max(logging.ERROR, GMOD_CONSOLE_LEVEL))
    gmod_console_stdout_handler.addFilter(StdoutFilter())
    gmod_console_stdout_handler.setFormatter(gmod_console_formatter)
    pygmod_logger.addHandler(gmod_console_stdout_handler)


def test():
    logger = logging.getLogger("pygmod")
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.fatal("fatal")
