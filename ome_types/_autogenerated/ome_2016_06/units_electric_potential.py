from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class UnitsElectricPotential(Enum):
    """
    The units used to represent an electric potential.

    Attributes
    ----------
    YOTTAVOLT : str
        yottavolt unit.
    ZETTAVOLT : str
        zettavolt unit.
    EXAVOLT : str
        exavolt unit.
    PETAVOLT : str
        petavolt unit.
    TERAVOLT : str
        teravolt unit.
    GIGAVOLT : str
        gigavolt unit.
    MEGAVOLT : str
        megavolt unit.
    KILOVOLT : str
        kilovolt unit.
    HECTOVOLT : str
        hectovolt unit.
    DECAVOLT : str
        decavolt unit.
    VOLT : str
        volt unit.
    DECIVOLT : str
        decivolt unit.
    CENTIVOLT : str
        centivolt unit.
    MILLIVOLT : str
        millivolt unit.
    MICROVOLT : str
        microvolt unit.
    NANOVOLT : str
        nanovolt unit.
    PICOVOLT : str
        picovolt unit.
    FEMTOVOLT : str
        femtovolt unit.
    ATTOVOLT : str
        attovolt unit.
    ZEPTOVOLT : str
        zeptovolt unit.
    YOCTOVOLT : str
        yoctovolt unit.
    """

    YOTTAVOLT = "YV"
    ZETTAVOLT = "ZV"
    EXAVOLT = "EV"
    PETAVOLT = "PV"
    TERAVOLT = "TV"
    GIGAVOLT = "GV"
    MEGAVOLT = "MV"
    KILOVOLT = "kV"
    HECTOVOLT = "hV"
    DECAVOLT = "daV"
    VOLT = "V"
    DECIVOLT = "dV"
    CENTIVOLT = "cV"
    MILLIVOLT = "mV"
    MICROVOLT = "µV"
    NANOVOLT = "nV"
    PICOVOLT = "pV"
    FEMTOVOLT = "fV"
    ATTOVOLT = "aV"
    ZEPTOVOLT = "zV"
    YOCTOVOLT = "yV"
