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
from .schema import to_dict, to_xml, validate  # isort:skip
from ._convenience import from_tiff, from_xml, from_bioformats  # isort:skip

__all__ = [
    "from_bioformats",
    "from_tiff",
    "from_xml",
    "model",
    "OME",
    "to_dict",
    "to_xml",
    "ureg",
    "validate",
]
