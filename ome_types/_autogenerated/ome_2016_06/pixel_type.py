from enum import Enum

from ome_types._mixins._validators import pixel_type_to_numpy_dtype

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class PixelType(Enum):
    """
    The number size/kind used to represent a pixel.

    Attributes
    ----------
    INT8 : str
        8 bit signed integer.
    INT16 : str
        16 bit signed integer.
    INT32 : str
        32 bit signed integer.
    UINT8 : str
        8 bit unsigned integer.
    UINT16 : str
        16 bit unsigned integer.
    UINT32 : str
        32 bit unsigned integer.
    FLOAT : str
        single-precision floating point.
    DOUBLE : str
        double-precision floating point.
    COMPLEXFLOAT : str
        complex single-precision floating point.
    COMPLEXDOUBLE : str
        complex double-precision floating point.
    BIT : str
        bit mask.
    """

    INT8 = "int8"
    INT16 = "int16"
    INT32 = "int32"
    UINT8 = "uint8"
    UINT16 = "uint16"
    UINT32 = "uint32"
    FLOAT = "float"
    DOUBLE = "double"
    COMPLEXFLOAT = "complex"
    COMPLEXDOUBLE = "double-complex"
    BIT = "bit"

    numpy_dtype = property(pixel_type_to_numpy_dtype)
