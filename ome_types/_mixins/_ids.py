from __future__ import annotations

import re
import warnings
from contextlib import suppress
from typing import TYPE_CHECKING, Any, cast

from ome_types._pydantic_compat import field_regex

if TYPE_CHECKING:
    from typing import Final

    from pydantic import BaseModel

# Default value to support automatic numbering for id field values.
AUTO_SEQUENCE: Final = "__auto_sequence__"
# map of id_name -> max id value
ID_COUNTER: dict[str, int] = {}

# map of (id_name, id_value) -> converted id
# NOTE: this is cleared in OMEMixin.__init__, so that the set of converted IDs
# is unique to each OME instance
CONVERTED_IDS: dict[tuple[str, str], str] = {}


def _get_id_name_and_pattern(cls: type[BaseModel]) -> tuple[str, str]:
    # let this raise if it doesn't exist...
    # this should only be used on classes that have an id field
    id_pattern = cast(str, field_regex(cls, "id"))
    id_name = id_pattern.split(":")[-3]
    return id_name, id_pattern


def validate_id(cls: type[BaseModel], value: int | str) -> Any:
    """Pydantic validator for ID fields in OME models.

    This validator does the following:
    1. if it's valid string ID just use it, and updating the counter if necessary.
    2. if it's an invalid string id, try to extract the integer part from it, and use
       that to create a new ID, or use the next value in the sequence if not.
    2. if it's an integer, grab the appropriate ID name from the pattern and prepend it.
    3. if it's the special `AUTO_SEQUENCE` sentinel, use the next value in the sequence.

    COUNTERS stores the maximum previously-seen value on the class.
    """
    id_name, id_pattern = _get_id_name_and_pattern(cls)
    current_count = ID_COUNTER.setdefault(id_name, -1)

    if value == AUTO_SEQUENCE:
        # if it's the special sentinel, use the next value
        value = ID_COUNTER[id_name] + 1
    elif isinstance(value, str):
        if (id_name, value) in CONVERTED_IDS:
            # XXX: possible bug
            # if the same invalid value is used across multiple documents
            # we'll be replacing it with the same converted id here
            return CONVERTED_IDS[(id_name, value)]

        # if the value is a string, extract the number from it if possible
        value_id: str = value.rsplit(":", 1)[-1]

        # if the value matches the pattern, just return it
        # but update the counter if it's higher than the current value
        if re.match(id_pattern, value):
            with suppress(ValueError):
                # (not all IDs have integers after the colon)
                ID_COUNTER[id_name] = max(current_count, int(value_id))
            return value

        # if the value doesn't match the pattern, create a proper ID
        # (using the value_id as the integer part if possible)
        id_int = int(value_id) if value_id.isdecimal() else current_count + 1
        newname = validate_id(cls, id_int)
        # store the converted ID so we can use it elsewhere
        CONVERTED_IDS[(id_name, value)] = newname

        # warn the user
        msg = f"Casting invalid {id_name}ID {value!r} to {newname!r}"
        warnings.warn(msg, stacklevel=2)
        return newname
    elif not isinstance(value, int):  # pragma: no cover
        raise ValueError(f"Invalid ID value: {value!r}, {type(value)}")

    # update the counter to be at least this value
    ID_COUNTER[id_name] = max(current_count, value)
    return f"{id_name}:{value}"
