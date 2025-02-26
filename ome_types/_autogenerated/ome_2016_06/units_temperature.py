from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class UnitsTemperature(Enum):
    """
    The units used to represent a temperature.

    Attributes
    ----------
    CELSIUS : str
        degree Celsius unit.
    FAHRENHEIT : str
        degree Fahrenheit unit.
    KELVIN : str
        Kelvin unit.
    RANKINE : str
        degree Rankine unit.
    """

    CELSIUS = "°C"
    FAHRENHEIT = "°F"
    KELVIN = "K"
    RANKINE = "°R"
