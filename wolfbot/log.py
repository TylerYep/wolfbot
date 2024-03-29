import logging
from pathlib import Path
from typing import Any

import prettyprinter  # type: ignore[import-untyped]
from prettyprinter.prettyprinter import IMPLICIT_MODULES  # type: ignore[import-untyped]


class Formatter:
    """Wrapper class for PrettyPrinter."""

    def __init__(self, prettyprinter_module: Any) -> None:
        self.pformat = prettyprinter_module.pformat
        self.pprint = prettyprinter_module.pprint


def init_prettyprinter() -> Formatter:
    """Initialize prettyprinter and add all IMPLICIT_MODULES."""
    prettyprinter.install_extras(include={"python", "dataclasses"})
    for filepath in Path("wolfbot").rglob("*.py"):
        module_name = filepath.stem
        if "__" not in module_name:
            prefix = ".".join(filepath.parts[:-1] + (module_name,))
            IMPLICIT_MODULES.add(prefix)
    return Formatter(prettyprinter)


class OneNightLogger:
    """
    Custom logger that caches all output.

    Logging Constants:
        TRACE = Debugging mode for development
        DEBUG = Include all hidden messages
        INFO = Regular gameplay
        WARNING = Results only
    """

    def __init__(self, filename: str = "") -> None:
        self.trace_level = 5
        if filename:
            logging.basicConfig(
                format="%(message)s",
                level=logging.DEBUG,
                filename=filename,
                filemode="a",
            )
        else:
            logging.basicConfig(format="%(message)s", level=logging.DEBUG)
        self.logger = logging.getLogger()
        self.output_cache: list[tuple[int, str]] = []

    def set_level(self, log_level: int) -> None:
        """Sets log level."""
        self.logger.setLevel(log_level)

    def clear(self) -> None:
        """Clears log cache."""
        self.output_cache.clear()

    def log(self, log_level: int, message: str, cache: bool = False) -> None:
        """Logs a line and saves that line if cache = True."""
        self.logger.log(log_level, message)
        if cache:
            self.output_cache.append((log_level, message))

    def trace(self, message: str, cache: bool = False) -> None:
        """Log function for TRACE output."""
        self.log(self.trace_level, message, cache)

    def info(self, message: str, cache: bool = False) -> None:
        """Log function for INFO output."""
        self.log(logging.INFO, message, cache)

    def debug(self, message: str, cache: bool = False) -> None:
        """Log function for DEBUG output."""
        self.log(logging.DEBUG, message, cache)

    def warning(self, message: str, cache: bool = False) -> None:
        """Log function for WARNING output."""
        self.log(logging.WARNING, message, cache)


formatter = init_prettyprinter()
logger = OneNightLogger()
