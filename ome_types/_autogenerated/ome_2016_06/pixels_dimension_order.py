from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Pixels_DimensionOrder(Enum):
    XYZCT = "XYZCT"
    XYZTC = "XYZTC"
    XYCTZ = "XYCTZ"
    XYCZT = "XYCZT"
    XYTCZ = "XYTCZ"
    XYTZC = "XYTZC"
