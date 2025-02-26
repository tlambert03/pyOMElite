from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("ome-types")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ome_types.units import ureg

from ome_types import model
from ome_types._conversion import from_tiff, from_xml, to_dict, to_xml, validate_xml
from ome_types.model import OME

__all__ = [
    "OME",
    "__version__",
    "from_tiff",
    "from_xml",
    "model",
    "to_dict",
    "to_xml",
    "ureg",
    "validate_xml",
]


def __getattr__(name: str) -> Any:
    if name == "ureg":
        from ome_types.units import ureg

        return ureg
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
