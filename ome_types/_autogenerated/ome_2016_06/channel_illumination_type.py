from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Channel_IlluminationType(Enum):
    TRANSMITTED = "Transmitted"
    EPIFLUORESCENCE = "Epifluorescence"
    OBLIQUE = "Oblique"
    NON_LINEAR = "NonLinear"
    OTHER = "Other"
