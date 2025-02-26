from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class UnitsPressure(Enum):
    """
    The units used to represent a pressure.

    Attributes
    ----------
    YOTTAPASCAL : str
        yottapascal SI unit.
    ZETTAPASCAL : str
        zettapascal SI unit.
    EXAPASCAL : str
        exapascal SI unit.
    PETAPASCAL : str
        petapascal SI unit.
    TERAPASCAL : str
        terapascal SI unit.
    GIGAPASCAL : str
        gigapascal SI unit.
    MEGAPASCAL : str
        megapascal SI unit.
    KILOPASCAL : str
        kilopascal SI unit.
    HECTOPASCAL : str
        hectopascal SI unit.
    DECAPASCAL : str
        decapascal SI unit.
    PASCAL : str
        pascal SI unit.  Note the C++ enum is mixed case due to PASCAL being a
        macro used by the Microsoft C and C++ compiler.
    DECIPASCAL : str
        decipascal SI unit.
    CENTIPASCAL : str
        centipascal SI unit.
    MILLIPASCAL : str
        millipascal SI unit.
    MICROPASCAL : str
        micropascal SI unit.
    NANOPASCAL : str
        nanopascal SI unit.
    PICOPASCAL : str
        picopascal SI unit.
    FEMTOPASCAL : str
        femtopascal SI unit.
    ATTOPASCAL : str
        attopascal SI unit.
    ZEPTOPASCAL : str
        zeptopascal SI unit.
    YOCTOPASCAL : str
        yoctopascal SI unit.
    BAR : str
        bar SI-derived unit.
    MEGABAR : str
        megabar SI-derived unit.
    KILOBAR : str
        kilobar SI-derived unit.
    DECIBAR : str
        decibar SI-derived unit.
    CENTIBAR : str
        centibar SI-derived unit.
    MILLIBAR : str
        millibar SI-derived unit.
    ATMOSPHERE : str
        standard atmosphere SI-derived unit.
    PSI : str
        pound-force per square inch Imperial unit.
    TORR : str
        torr SI-derived unit.
    MILLITORR : str
        millitorr SI-derived unit.
    MMHG : str
        millimetre of mercury SI-derived unit
    """

    YOTTAPASCAL = "YPa"
    ZETTAPASCAL = "ZPa"
    EXAPASCAL = "EPa"
    PETAPASCAL = "PPa"
    TERAPASCAL = "TPa"
    GIGAPASCAL = "GPa"
    MEGAPASCAL = "MPa"
    KILOPASCAL = "kPa"
    HECTOPASCAL = "hPa"
    DECAPASCAL = "daPa"
    PASCAL = "Pa"
    DECIPASCAL = "dPa"
    CENTIPASCAL = "cPa"
    MILLIPASCAL = "mPa"
    MICROPASCAL = "µPa"
    NANOPASCAL = "nPa"
    PICOPASCAL = "pPa"
    FEMTOPASCAL = "fPa"
    ATTOPASCAL = "aPa"
    ZEPTOPASCAL = "zPa"
    YOCTOPASCAL = "yPa"
    BAR = "bar"
    MEGABAR = "Mbar"
    KILOBAR = "kbar"
    DECIBAR = "dbar"
    CENTIBAR = "cbar"
    MILLIBAR = "mbar"
    ATMOSPHERE = "atm"
    PSI = "psi"
    TORR = "Torr"
    MILLITORR = "mTorr"
    MMHG = "mm Hg"
