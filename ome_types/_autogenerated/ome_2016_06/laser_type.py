from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Laser_Type(Enum):
    EXCIMER = "Excimer"
    GAS = "Gas"
    METAL_VAPOR = "MetalVapor"
    SOLID_STATE = "SolidState"
    DYE = "Dye"
    SEMICONDUCTOR = "Semiconductor"
    FREE_ELECTRON = "FreeElectron"
    OTHER = "Other"
