from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Channel_AcquisitionMode(Enum):
    WIDE_FIELD = "WideField"
    LASER_SCANNING_CONFOCAL_MICROSCOPY = "LaserScanningConfocalMicroscopy"
    SPINNING_DISK_CONFOCAL = "SpinningDiskConfocal"
    SLIT_SCAN_CONFOCAL = "SlitScanConfocal"
    MULTI_PHOTON_MICROSCOPY = "MultiPhotonMicroscopy"
    STRUCTURED_ILLUMINATION = "StructuredIllumination"
    SINGLE_MOLECULE_IMAGING = "SingleMoleculeImaging"
    TOTAL_INTERNAL_REFLECTION = "TotalInternalReflection"
    FLUORESCENCE_LIFETIME = "FluorescenceLifetime"
    SPECTRAL_IMAGING = "SpectralImaging"
    FLUORESCENCE_CORRELATION_SPECTROSCOPY = "FluorescenceCorrelationSpectroscopy"
    NEAR_FIELD_SCANNING_OPTICAL_MICROSCOPY = "NearFieldScanningOpticalMicroscopy"
    SECOND_HARMONIC_GENERATION_IMAGING = "SecondHarmonicGenerationImaging"
    PALM = "PALM"
    STORM = "STORM"
    STED = "STED"
    TIRF = "TIRF"
    FSM = "FSM"
    LCM = "LCM"
    OTHER = "Other"
    BRIGHT_FIELD = "BrightField"
    SWEPT_FIELD_CONFOCAL = "SweptFieldConfocal"
    SPIM = "SPIM"
