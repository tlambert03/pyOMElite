from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class UnitsTime(Enum):
    """
    The units used to represent a time interval.

    Attributes
    ----------
    YOTTASECOND : str
        yottasecond SI unit.
    ZETTASECOND : str
        zettasecond SI unit.
    EXASECOND : str
        exasecond SI unit.
    PETASECOND : str
        petasecond SI unit.
    TERASECOND : str
        terasecond SI unit.
    GIGASECOND : str
        gigasecond SI unit.
    MEGASECOND : str
        megasecond SI unit.
    KILOSECOND : str
        kilosecond SI unit.
    HECTOSECOND : str
        hectosecond SI unit.
    DECASECOND : str
        decasecond SI unit.
    SECOND : str
        second SI unit.
    DECISECOND : str
        decisecond SI unit.
    CENTISECOND : str
        centisecond SI unit.
    MILLISECOND : str
        millisecond SI unit.
    MICROSECOND : str
        microsecond SI unit.
    NANOSECOND : str
        nanosecond SI unit.
    PICOSECOND : str
        picosecond SI unit.
    FEMTOSECOND : str
        femtosecond SI unit.
    ATTOSECOND : str
        attosecond SI unit.
    ZEPTOSECOND : str
        zeptosecond SI unit.
    YOCTOSECOND : str
        yoctosecond SI unit.
    MINUTE : str
        minute SI-derived unit.
    HOUR : str
        hour SI-derived unit.
    DAY : str
        day SI-derived unit.
    """

    YOTTASECOND = "Ys"
    ZETTASECOND = "Zs"
    EXASECOND = "Es"
    PETASECOND = "Ps"
    TERASECOND = "Ts"
    GIGASECOND = "Gs"
    MEGASECOND = "Ms"
    KILOSECOND = "ks"
    HECTOSECOND = "hs"
    DECASECOND = "das"
    SECOND = "s"
    DECISECOND = "ds"
    CENTISECOND = "cs"
    MILLISECOND = "ms"
    MICROSECOND = "µs"
    NANOSECOND = "ns"
    PICOSECOND = "ps"
    FEMTOSECOND = "fs"
    ATTOSECOND = "as"
    ZEPTOSECOND = "zs"
    YOCTOSECOND = "ys"
    MINUTE = "min"
    HOUR = "h"
    DAY = "d"
