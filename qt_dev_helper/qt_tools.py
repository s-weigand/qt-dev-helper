"""Qt implementation cross compatibility module."""
from __future__ import annotations

import shutil
from functools import lru_cache
from pathlib import Path


class QtToolNotFoundError(Exception):
    """Error thrown when a Qt tool can't be found.

    See Also
    --------
    find_qt_tool
    """

    def __init__(self, tool_name: str) -> None:
        super().__init__(
            f"Can not find Qt tool {tool_name=} please install a Qt distributions. "
            "E.g. 'pip install PySide6'."
        )


@lru_cache()
def find_qt_tool(tool_name: str) -> str:
    """Find path to Qt tool executable like ``rcc``, ``uic`` or ``designer``.

    Parameters
    ----------
    tool_name: str
        Name of the Qt tool to look up.

    Returns
    -------
    str
        Path to the tool executable.

    Raises
    ------
    QtToolNotFoundError
        If the tool could not be found in the path.
    """
    known_prefixes = ["pyside6-", ""]
    for known_prefix in known_prefixes:
        command_path = shutil.which(f"{known_prefix}{tool_name}")
        if command_path is not None:
            return Path(tool_name).as_posix()
    raise QtToolNotFoundError(tool_name)
