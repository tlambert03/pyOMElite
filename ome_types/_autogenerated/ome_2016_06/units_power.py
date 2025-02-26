from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class UnitsPower(Enum):
    """
    The units used to represent power.

    Attributes
    ----------
    YOTTAWATT : str
        yottawatt unit.
    ZETTAWATT : str
        zettawatt unit.
    EXAWATT : str
        exawatt unit.
    PETAWATT : str
        petawatt unit.
    TERAWATT : str
        terawatt unit.
    GIGAWATT : str
        gigawatt unit.
    MEGAWATT : str
        megawatt unit.
    KILOWATT : str
        kilowatt unit.
    HECTOWATT : str
        hectowatt unit.
    DECAWATT : str
        decawatt unit.
    WATT : str
        watt unit.
    DECIWATT : str
        deciwatt unit.
    CENTIWATT : str
        centiwatt unit.
    MILLIWATT : str
        milliwatt unit.
    MICROWATT : str
        microwatt unit.
    NANOWATT : str
        nanowatt unit.
    PICOWATT : str
        picowatt unit.
    FEMTOWATT : str
        femtowatt unit.
    ATTOWATT : str
        attowatt unit.
    ZEPTOWATT : str
        zeptowatt unit.
    YOCTOWATT : str
        yoctowatt unit.
    """

    YOTTAWATT = "YW"
    ZETTAWATT = "ZW"
    EXAWATT = "EW"
    PETAWATT = "PW"
    TERAWATT = "TW"
    GIGAWATT = "GW"
    MEGAWATT = "MW"
    KILOWATT = "kW"
    HECTOWATT = "hW"
    DECAWATT = "daW"
    WATT = "W"
    DECIWATT = "dW"
    CENTIWATT = "cW"
    MILLIWATT = "mW"
    MICROWATT = "µW"
    NANOWATT = "nW"
    PICOWATT = "pW"
    FEMTOWATT = "fW"
    ATTOWATT = "aW"
    ZEPTOWATT = "zW"
    YOCTOWATT = "yW"
