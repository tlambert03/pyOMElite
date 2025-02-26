from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Shape_FontStyle(Enum):
    """The style and weight applied to the text.

    [enumeration] This is a simplified combination of the HTML/CSS
    attributes font-style AND font-weight.
    """

    BOLD = "Bold"
    BOLD_ITALIC = "BoldItalic"
    ITALIC = "Italic"
    NORMAL = "Normal"
