"""CLI utility functionality."""

from __future__ import annotations


def parse_optional_args_string(optional_args_string: str | None) -> list[str] | None:
    """Parse optional args string as comma separated list.

    Parameters
    ----------
    optional_args_string: str | None
        Optional argument string with coma separated arguments if not None.

    Returns
    -------
    list[str] |None
        None or list of arguments
    """
    if optional_args_string is None:
        return None
    args = [arg.strip() for arg in optional_args_string.split(",")]
    while "" in args:
        args.remove("")
    return args
