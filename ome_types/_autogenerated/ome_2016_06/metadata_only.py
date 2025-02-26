from ome_types._mixins._base_type import OMEType

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class MetadataOnly(OMEType):
    """This place holder means there is on pixel data in this file."""

    class Meta:
        namespace = "http://www.openmicroscopy.org/Schemas/OME/2016-06"
