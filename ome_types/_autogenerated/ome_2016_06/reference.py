from ome_types._mixins._base_type import OMEType
from ome_types._mixins._reference import ReferenceMixin

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Reference(ReferenceMixin, OMEType):
    """
    Reference is an empty complex type that is contained and extended by all the
    *Ref elements and also the Settings Complex Type Each *Ref element defines an
    attribute named ID of simple type *ID and no other information Each simple type
    *ID is restricted to the base type LSID with an appropriate pattern.
    """
