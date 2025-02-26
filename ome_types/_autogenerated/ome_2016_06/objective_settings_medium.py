from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class ObjectiveSettings_Medium(Enum):
    """A description of a Medium used for the lens.

    The Medium is the actual immersion medium used in this case.
    """

    AIR = "Air"
    OIL = "Oil"
    WATER = "Water"
    GLYCEROL = "Glycerol"
    OTHER = "Other"
