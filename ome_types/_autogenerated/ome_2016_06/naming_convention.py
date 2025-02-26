from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class NamingConvention(Enum):
    """
    Predefined list of values for the well labels.

    Attributes
    ----------
    LETTER : str
        While the label type 'number' has a clear meaning the 'letter' type is more
        complex. If you have less than 26 values use letters A to Z. Once you get
        more than 26 values there are several different approaches in use. One we
        have see include: Single letter, then double letter each running A to Z,
        right first e.g. A, B, C, ... X, Y, Z, AA, AB, AC, ... AY, AZ, BA, BB, ...
        This is the format used by Microsoft Excel so users may be familiar with
        it. This is the approach we use in the OMERO client applications.
        CAPITALsmall, each running A to Z, small first e.g. Aa, Ab, Ac, ... Ax, Ay,
        Az, Ba, Bb, Bc, ... By, Bz, Ca, Cb, ... This is in use by some plate
        manufactures. Single letter, then double letter, then triple letter, and so
        on e.g. A, B, C, ... X, Y, Z, AA, BB, CC, ... YY, ZZ, AAA, BBB, ... This
        has the advantage that the first 26 are the same as the standard but has a
        problem an the labels get wider and wider leading to user interface
        problems.
    NUMBER : str
        1, 2, 3, ...
    """

    LETTER = "letter"
    NUMBER = "number"
