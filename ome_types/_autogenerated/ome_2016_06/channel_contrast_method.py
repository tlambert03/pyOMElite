from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Channel_ContrastMethod(Enum):
    BRIGHTFIELD = "Brightfield"
    PHASE = "Phase"
    DIC = "DIC"
    HOFFMAN_MODULATION = "HoffmanModulation"
    OBLIQUE_ILLUMINATION = "ObliqueIllumination"
    POLARIZED_LIGHT = "PolarizedLight"
    DARKFIELD = "Darkfield"
    FLUORESCENCE = "Fluorescence"
    OTHER = "Other"
