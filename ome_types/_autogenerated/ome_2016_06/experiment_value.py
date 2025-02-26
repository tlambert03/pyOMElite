from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Experiment_value(Enum):
    FP = "FP"
    FRET = "FRET"
    TIME_LAPSE = "TimeLapse"
    FOUR_DPLUS = "FourDPlus"
    SCREEN = "Screen"
    IMMUNOCYTOCHEMISTRY = "Immunocytochemistry"
    IMMUNOFLUORESCENCE = "Immunofluorescence"
    FISH = "FISH"
    ELECTROPHYSIOLOGY = "Electrophysiology"
    ION_IMAGING = "IonImaging"
    COLOCALIZATION = "Colocalization"
    PGIDOCUMENTATION = "PGIDocumentation"
    FLUORESCENCE_LIFETIME = "FluorescenceLifetime"
    SPECTRAL_IMAGING = "SpectralImaging"
    PHOTOBLEACHING = "Photobleaching"
    SPIM = "SPIM"
    OTHER = "Other"
