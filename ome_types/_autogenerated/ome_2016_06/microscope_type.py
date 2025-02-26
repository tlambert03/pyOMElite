from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Microscope_Type(Enum):
    UPRIGHT = "Upright"
    INVERTED = "Inverted"
    DISSECTION = "Dissection"
    ELECTROPHYSIOLOGY = "Electrophysiology"
    OTHER = "Other"
