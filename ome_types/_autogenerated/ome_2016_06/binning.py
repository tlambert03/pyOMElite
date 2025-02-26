from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Binning(Enum):
    """Represents the number of pixels that are combined to form larger pixels.

    {used:CCD,EMCCD}

    Attributes
    ----------
    ONEBYONE : str
        No binning.
    TWOBYTWO : str
        2×2 binning.
    FOURBYFOUR : str
        4×4 binning.
    EIGHTBYEIGHT : str
        8×8 binning.
    OTHER : str
        Other binning value.
    """

    ONEBYONE = "1x1"
    TWOBYTWO = "2x2"
    FOURBYFOUR = "4x4"
    EIGHTBYEIGHT = "8x8"
    OTHER = "Other"
