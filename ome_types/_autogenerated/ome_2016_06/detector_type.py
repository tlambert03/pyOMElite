from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Detector_Type(Enum):
    CCD = "CCD"
    INTENSIFIED_CCD = "IntensifiedCCD"
    ANALOG_VIDEO = "AnalogVideo"
    PMT = "PMT"
    PHOTODIODE = "Photodiode"
    SPECTROSCOPY = "Spectroscopy"
    LIFETIME_IMAGING = "LifetimeImaging"
    CORRELATION_SPECTROSCOPY = "CorrelationSpectroscopy"
    FTIR = "FTIR"
    EMCCD = "EMCCD"
    APD = "APD"
    CMOS = "CMOS"
    EBCCD = "EBCCD"
    OTHER = "Other"
