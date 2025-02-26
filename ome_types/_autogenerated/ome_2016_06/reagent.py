from typing import Optional

from pydantic import Field

from ome_types._autogenerated.ome_2016_06.annotation_ref import AnnotationRef
from ome_types._mixins._base_type import OMEType

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Reagent(OMEType):
    """
    Reagent is used to describe a chemical or some other physical experimental
    parameter.

    Attributes
    ----------
    description : None | str
        A long description for the reagent.
    annotation_refs : list[AnnotationRef]
        (The Reagent AnnotationRefs).
    id : str
        (The Reagent ID).
    name : None | str
        A short name for the reagent
    reagent_identifier : None | str
        This is a reference to an external (to OME) representation of the Reagent.
        It serves as a foreign key into an external database. - It is sometimes
        referred to as ExternalIdentifier.
    """

    class Meta:
        namespace = "http://www.openmicroscopy.org/Schemas/OME/2016-06"

    description: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "name": "Description",
            "type": "Element",
            "white_space": "preserve",
        },
    )
    annotation_refs: list[AnnotationRef] = Field(
        default_factory=list,
        json_schema_extra={
            "name": "AnnotationRef",
            "type": "Element",
        },
    )
    id: str = Field(
        default="__auto_sequence__",
        pattern=r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Reagent:\S+)|(Reagent:\S+)",
        json_schema_extra={
            "name": "ID",
            "type": "Attribute",
            "required": True,
            "pattern": r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Reagent:\S+)|(Reagent:\S+)",
        },
    )
    name: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "name": "Name",
            "type": "Attribute",
        },
    )
    reagent_identifier: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "name": "ReagentIdentifier",
            "type": "Attribute",
        },
    )
