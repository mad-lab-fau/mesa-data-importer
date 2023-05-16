"""Some custom helper types to make type hints and type checking easier."""

from pathlib import Path
from typing import TypeVar

path_t = TypeVar("path_t", str, Path)  # pylint:disable=invalid-name
