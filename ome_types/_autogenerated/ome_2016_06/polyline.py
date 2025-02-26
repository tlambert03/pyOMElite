from typing import Optional

from pydantic import Field

from ome_types._autogenerated.ome_2016_06.marker import Marker
from ome_types._autogenerated.ome_2016_06.shape import Shape

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Polyline(Shape):
    """The Polyline defines open shapes formed of straight lines.

    Note: Polyline uses counterclockwise winding (this is the
    default OpenGL behavior)

    Attributes
    ----------
    points : str
        The points of the polyline are defined as a list of comma separated x,y
        coordinates seperated by spaces like "x1,y1 x2,y2 x3,y3" e.g. "0,0 1,2 3,5"
    marker_start : None | Marker
        (The Polyline MarkerStart).
    marker_end : None | Marker
        (The Polyline MarkerEnd).
    """

    class Meta:
        namespace = "http://www.openmicroscopy.org/Schemas/OME/2016-06"

    points: str = Field(
        json_schema_extra={
            "name": "Points",
            "type": "Attribute",
            "required": True,
        }
    )
    marker_start: Optional[Marker] = Field(
        default=None,
        json_schema_extra={
            "name": "MarkerStart",
            "type": "Attribute",
        },
    )
    marker_end: Optional[Marker] = Field(
        default=None,
        json_schema_extra={
            "name": "MarkerEnd",
            "type": "Attribute",
        },
    )
