from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Filter_Type(Enum):
    DICHROIC = "Dichroic"
    LONG_PASS = "LongPass"
    SHORT_PASS = "ShortPass"
    BAND_PASS = "BandPass"
    MULTI_PASS = "MultiPass"
    NEUTRAL_DENSITY = "NeutralDensity"
    TUNEABLE = "Tuneable"
    OTHER = "Other"
