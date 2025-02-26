import weakref
from typing import Any, Optional, Union

from pydantic import PrivateAttr

from ome_types._mixins._base_type import OMEType


class ReferenceMixin(OMEType):
    _ref: Optional[weakref.ReferenceType] = PrivateAttr(None)

    @property
    def ref(self) -> Union[OMEType, None]:
        if self._ref is None:
            raise ValueError("references not yet resolved on root OME object")
        return self._ref()

    def __getstate__(self: Any) -> dict[str, Any]:
        """Support pickle of our weakref references."""
        state = super().__getstate__()
        if "__private_attribute_values__" in state:
            state["__private_attribute_values__"].pop("_ref", None)
        elif "__pydantic_private__" in state:
            state["__pydantic_private__"].pop("_ref", None)
        return state
