"""Configuration module."""

from pathlib import Path
from typing import Any
from typing import Dict
from typing import Tuple
from typing import Union

import tomli
from pydantic import BaseSettings
from pydantic import Field
from pydantic import root_validator
from pydantic import validator


class Config(BaseSettings):
    """Project configuration file."""

    base_path: Path = Field(
        description="Directory the config was loaded from, used to resolve relative paths."
    )
    root_sass_file: Union[str, None] = Field(default=None, description="")
    root_qss_file: Union[str, None] = None

    @validator("root_sass_file")
    def _validate_sass_path(
        cls: "Config", root_sass_file: str, values: Dict[str, Any]
    ) -> Union[str, None]:
        """Validate that ``root_sass_file`` is a valid path if defined."""
        if root_sass_file is None:
            return None
        root_sass_file_path: Path = values["base_path"] / root_sass_file
        if not root_sass_file_path.is_file():
            raise ValueError("The value of 'root_sass_file' needs to be a valid path or None.")
        return root_sass_file

    @root_validator()
    def _validate_styles(cls: "Config", values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that ``root_sass_file`` and ``root_qss_file`` are both defined or undefined."""
        root_sass_file = values.get("root_sass_file")
        root_qss_file = values.get("root_qss_file")
        if (root_qss_file is None and root_sass_file is not None) or (
            root_qss_file is not None and root_sass_file is None
        ):
            raise ValueError(
                "The values of 'root_qss_file' and 'root_sass_file' need either be both "
                f"defined or both be undefined.\nGot:\n\t{root_qss_file=}\n\t{root_sass_file=}"
            )
        return values

    def root_style_paths(self) -> Tuple[Path, Path]:
        """Resolve paths to root style files.

        Returns
        -------
        Tuple[Path, Path]
            Paths to ``root_sass_file`` and ``root_qss_file``.

        Raises
        ------
        ValueError
            If any root style file is not defined.
        """
        if self.root_sass_file is None or self.root_qss_file is None:
            raise ValueError(
                "Both 'root_qss_file' and 'root_sass_file' need to be defined.\n"
                f"Got:\n\t{self.root_qss_file=}\n\n{self.root_sass_file=}"
            )
        return self.base_path / self.root_sass_file, self.base_path / self.root_qss_file


def load_toml_config(path: Path) -> Config:
    """Load config from toml config file.

    Parameters
    ----------
    path: Path
        Path to the toml config file.

    Returns
    -------
    Config
        Configuration instance generate from toml definition.
    """
    toml_config = tomli.loads(path.read_text())
    if "tool" not in toml_config and "qt-dev-helper" not in toml_config["tool"]:
        return Config(base_path=path.parent)
    return Config(**{**toml_config["tool"]["qt-dev-helper"], "base_path": path.parent})
