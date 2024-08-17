"""Configuration module."""

from __future__ import annotations

import os
from enum import Enum
from pathlib import Path
from typing import Any
from typing import Literal
from typing import TypedDict

import tomli
from pydantic import Field
from pydantic import model_validator
from pydantic_settings import BaseSettings


class QtDevHelperConfigError(Exception):
    """Error thrown when accessing functionality with insufficient config."""


class ConfigNotFoundError(Exception):
    """Error thrown when the config file could not be found."""


def _str_list_factory(*args: Any) -> list[str]:
    """Ensure that a list of arbitrary argument is list[str].

    Parameters
    ----------
    *args : Any
        Arbitrary arguments.

    Returns
    -------
    list[str]
        List of ``args`` cast to string.
    """
    return [str(arg) for arg in args]


def _check_symmetric_io_definition(
    config: Config, input_var_name: str, output_var_name: str
) -> Config:
    """Check that ``input_var_name`` and ``output_var_name`` are both None or both not None.

    Parameters
    ----------
    config : "Config"
        Instance of the Config.
    input_var_name : str
        Name of the input path variable.
    output_var_name : str
        Name of the output path variable.

    Returns
    -------
    "Config"
        Value of ``values``

    Raises
    ------
    AssertionError
        If only one value of ``input_var_name`` and ``output_var_name`` is None.
    """
    input_path = config.model_dump().get(input_var_name)
    output_path = config.model_dump().get(output_var_name)
    if (output_path is None and input_path is not None) or (
        output_path is not None and input_path is None
    ):
        msg = (
            f"The values of {input_var_name!r} and {output_var_name!r} "
            "need either be both defined or both be undefined.\n"
            "Got:\n\t{input_var_name}={input_path!r}\n\t{output_var_name}={output_path!r}"
        )
        raise AssertionError(msg)
    return config


def _check_input_exists(
    config_dict: dict[str, Any], input_var_name: str, *, is_file: bool = False
) -> dict[str, Any]:
    """Check that the input path ``config.base_path / input_var`` exists.

    Parameters
    ----------
    config_dict : dict[str, Any]
        Dict of the Config.
    input_var_name : str
        Variable name, used to get value and format the error message.
    is_file : bool
        Whether to check if the path is a valid file or folder. Defaults to False

    Returns
    -------
    dict[str, Any]
        Value of ``input_var``

    Raises
    ------
    ValueError
        If ``is_file`` is True and the path is not a file.
    ValueError
        If ``is_file`` is False and the path is not a folder.
    """
    input_var = config_dict.get(input_var_name)
    if input_var is None:
        return config_dict
    input_var_path: Path = config_dict.get("base_path") / input_var
    if (
        is_file is True
        and not input_var_path.is_file()
        or is_file is not True
        and not input_var_path.is_dir()
    ):
        exception_msg = f"The value of {input_var_name!r} needs to be a valid path or None."
        raise ValueError(exception_msg)
    return config_dict


def expand_io_paths(
    config: Config, input_var_name: str, output_var_name: str
) -> tuple[Path, Path]:
    """Expand relative io paths with ``base_path`` from config.

    Parameters
    ----------
    config : Config
        Config instance, needed to determine the base path.
    input_var_name : str
        Name of the variable holding the input path string.
    output_var_name : str
        Name of the variable holding the input path string.

    Returns
    -------
    tuple[Path, Path]
        Expanded input path and expanded output path.

    Raises
    ------
    QtDevHelperConfigError
        If any of the io paths is None.
    """
    input_var: str = getattr(config, input_var_name)
    output_var: str = getattr(config, output_var_name)
    base_path: Path = config.base_path
    if input_var is None or output_var is None:
        msg = (
            f"Both {input_var_name!r} and {output_var_name!r} need to be defined.\n"
            "Got:\n\t{input_var_name}={output_var!r}\n\n{input_var_name}={output_var!r}"
        )
        raise QtDevHelperConfigError(msg)
    return base_path / input_var, base_path / output_var


class CodeGenerators(str, Enum):
    """Valid code generator values."""

    python = "python"
    cpp = "cpp"


class UicKwargs(TypedDict, total=False):
    """Keyword arguments to be used with ``compile_ui_file``."""

    generator: Literal["python", "cpp"]
    uic_args: list[str]
    form_import: bool


class RccKwargs(TypedDict, total=False):
    """Keyword arguments to be used with ``compile_resource_file``."""

    generator: Literal["python", "cpp"]
    rcc_args: list[str]


class Config(BaseSettings, extra="forbid"):  # type:ignore[call-arg]
    """Project configuration."""

    base_path: Path = Field(
        description="Directory the config was loaded from, used to resolve relative paths."
    )
    # Style generator options
    root_sass_file: str | None = Field(
        default=None, description="Scss stylesheet with the style for the whole application."
    )
    root_qss_file: str | None = Field(
        default=None,
        description=(
            "Qss stylesheet with the style for the whole application, "
            "generated from 'root_sass_file'."
        ),
    )
    # General Qt code generator options
    generator: CodeGenerators = Field(
        default=CodeGenerators.python,
        description="Code generator used to compile ui and resource files.",
    )
    flatten_folder_structure: bool = Field(
        default=True, description="Whether to keep the original folder structure or flatten it."
    )
    # Qt ui code generator options
    ui_files_folder: str | None = Field(
        default=None, description="Root folder containing *.ui files."
    )
    generated_ui_code_folder: str | None = Field(
        default=None, description="Root folder to save code generated from *.ui files to."
    )
    uic_args: list[str] = Field(
        default_factory=_str_list_factory,
        description="Additional arguments for the uic executable.",
    )
    form_import: bool = Field(default=True, description="Python: generate imports relative to '.'")
    # Qt rc code generator options
    resource_folder: str | None = Field(
        default=None, description="Root folder containing *.qrc files."
    )
    generated_rc_code_folder: str | None = Field(
        default=None, description="Root folder to save code generated from *.qrc files to."
    )
    rcc_args: list[str] = Field(
        default_factory=_str_list_factory,
        description="Additional arguments for the rcc executable.",
    )

    @model_validator(mode="before")
    def _validate_style_input_path(  # noqa: DOC
        cls: type[Config], data: dict[str, Any]
    ) -> dict[str, Any]:
        """Validate that ``root_sass_file`` is a valid path if defined."""
        return _check_input_exists(data, "root_sass_file", is_file=True)

    @model_validator(mode="before")
    def _validate_ui_input_path(  # noqa: DOC
        cls: type[Config], data: dict[str, Any]
    ) -> dict[str, Any]:
        """Validate that ``ui_files_folder`` is a valid path if defined."""
        return _check_input_exists(data, "ui_files_folder")

    @model_validator(mode="before")
    def _validate_rc_input_path(  # noqa: DOC
        cls: type[Config], data: dict[str, Any]
    ) -> dict[str, Any]:
        """Validate that ``resource_folder`` is a valid path if defined."""
        return _check_input_exists(data, "resource_folder")

    @model_validator(mode="after")
    def _validate_styles_io(self) -> Config:  # noqa: DOC
        """``root_sass_file`` and ``root_qss_file`` are both defined or undefined."""
        return _check_symmetric_io_definition(self, "root_sass_file", "root_qss_file")

    @model_validator(mode="after")
    def _validate_ui_io(self) -> Config:  # noqa: DOC
        """``ui_files_folder`` and ``generated_ui_code_folder`` are both defined or undefined."""
        return _check_symmetric_io_definition(self, "ui_files_folder", "generated_ui_code_folder")

    @model_validator(mode="after")
    def _validate_rc_io(self) -> Config:  # noqa: DOC
        """``resource_folder`` and ``generated_rc_code_folder`` are both defined or undefined."""
        return _check_symmetric_io_definition(self, "resource_folder", "generated_rc_code_folder")

    def root_style_paths(self) -> tuple[Path, Path]:
        """Resolve paths to root style files.

        Returns
        -------
        tuple[Path, Path]
            Paths to ``root_sass_file`` and ``root_qss_file``.
        """
        return expand_io_paths(self, "root_sass_file", "root_qss_file")

    def ui_folder_paths(self) -> tuple[Path, Path]:
        """Resolve paths to root style files.

        Returns
        -------
        tuple[Path, Path]
            Paths to ``ui_files_folder`` and ``generated_ui_code_folder``.
        """
        return expand_io_paths(self, "ui_files_folder", "generated_ui_code_folder")

    def rc_folder_paths(self) -> tuple[Path, Path]:
        """Resolve paths to root style files.

        Returns
        -------
        tuple[Path, Path]
            Paths to ``resource_folder`` and ``generated_rc_code_folder``.
        """
        return expand_io_paths(self, "resource_folder", "generated_rc_code_folder")

    def uic_kwargs(self) -> UicKwargs:
        """Extract keyword arguments to be used with ``compile_ui_file``.

        Returns
        -------
        UicKwargs
            Keyword arguments for ``compile_ui_file``.
        """
        return {
            "generator": self.generator.value,
            "form_import": self.form_import,
            "uic_args": self.uic_args,
        }

    def rcc_kwargs(self) -> RccKwargs:
        """Extract keyword arguments to be used with ``compile_resource_file``.

        Returns
        -------
        RccKwargs
            Keyword arguments for ``compile_resource_file``.
        """
        return {
            "generator": self.generator.value,
            "rcc_args": self.rcc_args,
        }

    def deactivate_style_build(self) -> None:
        """Deactivate style building with :func:`build_all_assets`."""
        self.root_sass_file = None
        self.root_qss_file = None

    def deactivate_ui_build(self) -> None:
        """Deactivate ui building with :func:`build_all_assets`."""
        self.ui_files_folder = None
        self.generated_ui_code_folder = None

    def deactivate_resource_build(self) -> None:
        """Deactivate resource building with :func:`build_all_assets`."""
        self.resource_folder = None
        self.generated_rc_code_folder = None

    def update(self, update_dict: dict[str, Any], *, filter_none: bool = True) -> None:
        """Update config values.

        Parameters
        ----------
        update_dict : dict[str, Any]
            Dict containing updated values.
        filter_none : bool
            Whether or not to filter None values before updating. Defaults to True
        """
        if filter_none is True:
            update_dict = {key: value for key, value in update_dict.items() if value is not None}

        # This ensures validation of the updated values
        updated_config = self.__class__(**{**self.model_dump(), **update_dict})

        for key, val in updated_config.model_dump().items():
            setattr(self, key, val)


def load_toml_config(path: Path) -> Config:
    """Load config from toml config file.

    Parameters
    ----------
    path : Path
        Path to the toml config file.

    Returns
    -------
    Config
        Configuration instance generate from toml definition.

    Raises
    ------
    ConfigNotFoundError
        If no config file does not contain 'qt-dev-helper' config.
    """
    toml_config = tomli.loads(path.read_text())
    qt_dev_helper_config = toml_config.get("tool", {}).get("qt-dev-helper", {})
    if len(qt_dev_helper_config) > 0:
        return Config.model_validate({**qt_dev_helper_config, "base_path": path.parent})
    msg = f"Could not find 'qt-dev-helper' config in {path.as_posix()}"
    raise ConfigNotFoundError(msg)


def find_config(
    start_path: Path | str | None = None, config_file_name: str = "pyproject.toml"
) -> Path:
    """Find config file based on its name and start path, by traversing parent paths.

    Parameters
    ----------
    start_path : Path | str | None
        Path to start looking for the config file.
        Defaults to None which means the current dir will be used
    config_file_name : str
        Name of the config file. Defaults to "pyproject.toml"

    Returns
    -------
    Path
        Path of the found config file

    Raises
    ------
    ConfigNotFoundError
        If no config file could be found.
    """
    if start_path is None:
        start_path = Path(os.curdir)

    start_path = Path(start_path).resolve()
    if start_path.is_file():
        start_path = start_path.parent

    for path in (start_path, *start_path.parents):
        file_path = path / config_file_name
        if file_path in set(path.iterdir()):
            return file_path
    msg = f"Could not find config file {config_file_name!r}."
    raise ConfigNotFoundError(msg)


def load_config(start_path: Path | str | None = None) -> Config:
    """Load config from file.

    Parameters
    ----------
    start_path : Path | str | None
        Path to start looking for the config file.
        Defaults to None which means the current dir will be used

    Returns
    -------
    Config
        Configuration instance generated from file.

    Raises
    ------
    ConfigNotFoundError
        If no config file containing 'qt-dev-helper' config could be found.
    """
    supported_config_formats = (("pyproject.toml", load_toml_config),)
    for config_file_name, load_func in supported_config_formats:
        try:
            return load_func(find_config(start_path, config_file_name))
        except ConfigNotFoundError:
            continue

    msg = "No config file containing 'qt-dev-helper' config could be found."
    raise ConfigNotFoundError(msg)
