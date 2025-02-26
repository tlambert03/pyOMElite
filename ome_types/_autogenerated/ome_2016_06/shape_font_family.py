from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Shape_FontFamily(Enum):
    """The font family used to draw the text.

    [enumeration]
    Note: these values are all lower case so they match
    the standard HTML/CSS values. "fantasy" has been
    included for completeness; we do not recommend its
    regular use. This attribute is under consideration
    for removal from the OME-XML schema.
    """

    SERIF = "serif"
    SANS_SERIF = "sans-serif"
    CURSIVE = "cursive"
    FANTASY = "fantasy"
    MONOSPACE = "monospace"
