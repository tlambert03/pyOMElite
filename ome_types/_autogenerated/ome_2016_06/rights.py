from typing import Optional

from pydantic import Field

from ome_types._mixins._base_type import OMEType

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Rights(OMEType):
    """
    The rights holder of this data and the rights held.

    Attributes
    ----------
    rights_holder : None | str
        The rights holder for this data. [plain-text multi-line string] e.g.
        "Copyright (C) 2002 - 2016 Open Microscopy Environment"
    rights_held : None | str
        The rights held by the rights holder. [plain-text multi-line string] e.g.
        "All rights reserved" or "Creative Commons Attribution 3.0 Unported
        License"
    """

    class Meta:
        namespace = "http://www.openmicroscopy.org/Schemas/OME/2016-06"

    rights_holder: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "name": "RightsHolder",
            "type": "Element",
            "white_space": "preserve",
        },
    )
    rights_held: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "name": "RightsHeld",
            "type": "Element",
            "white_space": "preserve",
        },
    )
