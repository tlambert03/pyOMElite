from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Objective_Immersion(Enum):
    OIL = "Oil"
    WATER = "Water"
    WATER_DIPPING = "WaterDipping"
    AIR = "Air"
    MULTI = "Multi"
    GLYCEROL = "Glycerol"
    OTHER = "Other"
