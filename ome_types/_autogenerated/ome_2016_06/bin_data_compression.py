from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class BinData_Compression(Enum):
    ZLIB = "zlib"
    BZIP2 = "bzip2"
    NONE = "none"
