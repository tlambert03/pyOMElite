from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class MicrobeamManipulation_value(Enum):
    FRAP = "FRAP"
    FLIP = "FLIP"
    INVERSE_FRAP = "InverseFRAP"
    PHOTOABLATION = "Photoablation"
    PHOTOACTIVATION = "Photoactivation"
    UNCAGING = "Uncaging"
    OPTICAL_TRAPPING = "OpticalTrapping"
    OTHER = "Other"
