from ._units import ureg

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

try:
    from . import model
    from .model import OME
except ModuleNotFoundError as e:
    raise ModuleNotFoundError(
        "Could not import 'ome_types.model.OME'.\nIf you are in a dev environment, "
        "you may need to run 'python -m src.ome_autogen'" + str(e)
    ) from None

from ._convenience import (  # isort:skip
    from_tiff,
    from_xml,
    to_dict,
    to_xml,
    validate_xml,
)

__all__ = [
    "to_dict",
    "validate_xml",
    "from_xml",
    "to_xml",
    "from_tiff",
    "OME",
    "model",
    "ureg",
]
