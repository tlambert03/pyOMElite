from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Arc_Type(Enum):
    HG = "Hg"
    XE = "Xe"
    HG_XE = "HgXe"
    OTHER = "Other"
