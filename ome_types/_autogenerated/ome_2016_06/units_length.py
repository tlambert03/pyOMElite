from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class UnitsLength(Enum):
    """
    The units used to represent a length.

    Attributes
    ----------
    YOTTAMETER : str
        yottameter SI unit.
    ZETTAMETER : str
        zettameter SI unit.
    EXAMETER : str
        exameter SI unit.
    PETAMETER : str
        petameter SI unit.
    TERAMETER : str
        terameter SI unit.
    GIGAMETER : str
        gigameter SI unit.
    MEGAMETER : str
        megameter SI unit.
    KILOMETER : str
        kilometer SI unit.
    HECTOMETER : str
        hectometer SI unit.
    DECAMETER : str
        decameter SI unit.
    METER : str
        meter SI unit.
    DECIMETER : str
        decimeter SI unit.
    CENTIMETER : str
        centimeter SI unit.
    MILLIMETER : str
        millimeter SI unit.
    MICROMETER : str
        micrometer SI unit.
    NANOMETER : str
        nanometer SI unit.
    PICOMETER : str
        picometer SI unit.
    FEMTOMETER : str
        femtometer SI unit.
    ATTOMETER : str
        attometer SI unit.
    ZEPTOMETER : str
        zeptometer SI unit.
    YOCTOMETER : str
        yoctometer SI unit.
    ANGSTROM : str
        ångström SI-derived unit.
    THOU : str
        thou Imperial unit (or mil, 1/1000 inch).
    LINE : str
        line Imperial unit (1/12 inch).
    INCH : str
        inch Imperial unit.
    FOOT : str
        foot Imperial unit.
    YARD : str
        yard Imperial unit.
    MILE : str
        terrestrial mile Imperial unit.
    ASTRONOMICALUNIT : str
        astronomical unit SI-derived unit. The official term is ua as the SI
        standard assigned AU to absorbance unit.
    LIGHTYEAR : str
        light year.
    PARSEC : str
        parsec.
    POINT : str
        typography point Imperial-derived unit (1/72 inch). Use of this unit should
        be limited to font sizes.
    PIXEL : str
        pixel abstract unit.  This is not convertible to any other length unit
        without a calibrated scaling factor. Its use should should be limited to
        ROI objects, and converted to an appropriate length units using the
        PhysicalSize units of the Image the ROI is attached to.
    REFERENCEFRAME : str
        reference frame abstract unit.  This is not convertible to any other length
        unit without a scaling factor.  Its use should be limited to uncalibrated
        stage positions, and converted to an appropriate length unit using a
        calibrated scaling factor.
    """

    YOTTAMETER = "Ym"
    ZETTAMETER = "Zm"
    EXAMETER = "Em"
    PETAMETER = "Pm"
    TERAMETER = "Tm"
    GIGAMETER = "Gm"
    MEGAMETER = "Mm"
    KILOMETER = "km"
    HECTOMETER = "hm"
    DECAMETER = "dam"
    METER = "m"
    DECIMETER = "dm"
    CENTIMETER = "cm"
    MILLIMETER = "mm"
    MICROMETER = "µm"
    NANOMETER = "nm"
    PICOMETER = "pm"
    FEMTOMETER = "fm"
    ATTOMETER = "am"
    ZEPTOMETER = "zm"
    YOCTOMETER = "ym"
    ANGSTROM = "Å"
    THOU = "thou"
    LINE = "li"
    INCH = "in"
    FOOT = "ft"
    YARD = "yd"
    MILE = "mi"
    ASTRONOMICALUNIT = "ua"
    LIGHTYEAR = "ly"
    PARSEC = "pc"
    POINT = "pt"
    PIXEL = "pixel"
    REFERENCEFRAME = "reference frame"
