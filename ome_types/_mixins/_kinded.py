import builtins
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, model_serializer


class KindMixin(BaseModel):
    """Mixin to a `kind` field to the dict output.

    This helps for casting a dict to a specific subclass, when the fields are
    otherwise identical.
    """

    def __init__(self, **data: Any) -> None:
        data.pop("kind", None)
        return super().__init__(**data)

    if not TYPE_CHECKING:

        def model_dump(self, **kwargs: Any) -> dict[str, Any]:
            d = super().model_dump(**kwargs)
            d["kind"] = self.__class__.__name__.lower()
            return d

    @model_serializer(mode="wrap")
    def serialize_root(self, handler, _info) -> builtins.dict:  # type: ignore
        d = handler(self)
        d["kind"] = self.__class__.__name__.lower()
        return d
