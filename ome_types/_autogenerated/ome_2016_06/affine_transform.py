from pydantic import Field

from ome_types._mixins._base_type import OMEType

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class AffineTransform(OMEType):
    """A matrix used to transform the shape.

    ⎡ A00, A01, A02 ⎤ ⎢ A10, A11, A12 ⎥ ⎣ 0,   0,   1   ⎦
    """

    a00: float = Field(
        json_schema_extra={
            "name": "A00",
            "type": "Attribute",
            "required": True,
        }
    )
    a10: float = Field(
        json_schema_extra={
            "name": "A10",
            "type": "Attribute",
            "required": True,
        }
    )
    a01: float = Field(
        json_schema_extra={
            "name": "A01",
            "type": "Attribute",
            "required": True,
        }
    )
    a11: float = Field(
        json_schema_extra={
            "name": "A11",
            "type": "Attribute",
            "required": True,
        }
    )
    a02: float = Field(
        json_schema_extra={
            "name": "A02",
            "type": "Attribute",
            "required": True,
        }
    )
    a12: float = Field(
        json_schema_extra={
            "name": "A12",
            "type": "Attribute",
            "required": True,
        }
    )
