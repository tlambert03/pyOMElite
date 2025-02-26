from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Shape_FillRule(Enum):
    """The rule used to decide which parts of the shape to fill.

    [enumeration]
    """

    EVEN_ODD = "EvenOdd"
    NON_ZERO = "NonZero"
