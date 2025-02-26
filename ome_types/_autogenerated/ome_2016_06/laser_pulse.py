from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Laser_Pulse(Enum):
    CW = "CW"
    SINGLE = "Single"
    QSWITCHED = "QSwitched"
    REPETITIVE = "Repetitive"
    MODE_LOCKED = "ModeLocked"
    OTHER = "Other"
