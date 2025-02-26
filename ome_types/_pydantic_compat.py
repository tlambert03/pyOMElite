from __future__ import annotations

from collections.abc import MutableSequence
from typing import TYPE_CHECKING, Any

import pydantic.version
from pydantic import BaseModel
from pydantic_extra_types.color import Color as Color

if TYPE_CHECKING:
    from pydantic.fields import FieldInfo

pydantic_version: tuple[int, ...] = tuple(
    int(x) for x in pydantic.version.VERSION.split(".")[:2]
)


def field_type(field: FieldInfo) -> Any:
    return field.annotation


def field_regex(obj: type[BaseModel], field_name: str) -> str | None:
    # typing is incorrect at the moment, but may indicate breakage in pydantic 3
    field_info = obj.model_fields[field_name]  # type: ignore [index]
    meta = field_info.json_schema_extra or {}
    if meta:
        return meta.get("pattern")  # type: ignore
    return None  # pragma: no cover


kw: dict = {"validated_data": {}} if pydantic_version >= (2, 10) else {}


def get_default(f: FieldInfo) -> Any:
    return f.get_default(call_default_factory=True, **kw)


def update_set_fields(self: BaseModel) -> None:
    """Update set fields with populated mutable sequences.

    Because pydantic isn't aware of mutations to sequences, it can't tell when
    a field has been "set" by mutating a sequence.  This method updates the
    `model_fields_set` attribute to reflect that.  We assume that if an attribute
    is not None, and is not equal to the default value, then it has been set.
    """
    for field_name, field in self.model_fields.items():
        current = getattr(self, field_name)
        if not current:
            continue
        if current != get_default(field):
            self.model_fields_set.add(field_name)
        if isinstance(current, BaseModel):
            update_set_fields(current)
        if isinstance(current, MutableSequence):
            for item in current:
                if isinstance(item, BaseModel):
                    update_set_fields(item)
