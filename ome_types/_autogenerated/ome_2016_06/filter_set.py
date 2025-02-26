from typing import Optional

from pydantic import Field

from ome_types._autogenerated.ome_2016_06.dichroic_ref import DichroicRef
from ome_types._autogenerated.ome_2016_06.filter_ref import FilterRef
from ome_types._autogenerated.ome_2016_06.manufacturer_spec import (
    ManufacturerSpec,
)

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class FilterSet(ManufacturerSpec):
    """
    Filter set manufacturer specification.

    Attributes
    ----------
    excitation_filters : list[FilterRef]
        The Filters placed in the Excitation light path.
    dichroic_ref : None | DichroicRef
        (The FilterSet DichroicRef).
    emission_filters : list[FilterRef]
        The Filters placed in the Emission light path.
    id : str
        (The FilterSet ID).
    """

    class Meta:
        namespace = "http://www.openmicroscopy.org/Schemas/OME/2016-06"

    excitation_filters: list[FilterRef] = Field(
        default_factory=list,
        json_schema_extra={
            "name": "ExcitationFilterRef",
            "type": "Element",
        },
    )
    dichroic_ref: Optional[DichroicRef] = Field(
        default=None,
        json_schema_extra={
            "name": "DichroicRef",
            "type": "Element",
        },
    )
    emission_filters: list[FilterRef] = Field(
        default_factory=list,
        json_schema_extra={
            "name": "EmissionFilterRef",
            "type": "Element",
        },
    )
    id: str = Field(
        default="__auto_sequence__",
        pattern=r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:FilterSet:\S+)|(FilterSet:\S+)",
        json_schema_extra={
            "name": "ID",
            "type": "Attribute",
            "required": True,
            "pattern": r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:FilterSet:\S+)|(FilterSet:\S+)",
        },
    )
