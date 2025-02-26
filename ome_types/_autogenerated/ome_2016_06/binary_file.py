from typing import Optional

from pydantic import Field

from ome_types._autogenerated.ome_2016_06.bin_data import BinData
from ome_types._autogenerated.ome_2016_06.external import External
from ome_types._mixins._base_type import OMEType

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class BinaryFile(OMEType):
    """
    Describes a binary file.

    Attributes
    ----------
    external : None | External
        (The BinaryFile External).
    bin_data : None | BinData
        (The BinaryFile BinData).
    file_name : str
        (The BinaryFile FileName).
    size : int
        Size of the uncompressed file. [unit:bytes]
    mime_type : None | str
        (The BinaryFile MIMEType).
    """

    class Meta:
        namespace = "http://www.openmicroscopy.org/Schemas/OME/2016-06"

    external: Optional[External] = Field(
        default=None,
        json_schema_extra={
            "name": "External",
            "type": "Element",
        },
    )
    bin_data: Optional[BinData] = Field(
        default=None,
        json_schema_extra={
            "name": "BinData",
            "type": "Element",
        },
    )
    file_name: str = Field(
        json_schema_extra={
            "name": "FileName",
            "type": "Attribute",
            "required": True,
        }
    )
    size: int = Field(
        ge=0,
        json_schema_extra={
            "name": "Size",
            "type": "Attribute",
            "required": True,
            "min_inclusive": 0,
        },
    )
    mime_type: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "name": "MIMEType",
            "type": "Attribute",
        },
    )
