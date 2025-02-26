from __future__ import annotations

from typing import TYPE_CHECKING, Any

try:
    import pint
except ImportError:  # pragma: no cover
    raise ImportError(
        "Pint is required to use quantities in ome-types. "
        "Install with `pip install ome-types[pint]`."
    ) from None


if TYPE_CHECKING:
    from pydantic import BaseModel

# The [`pint.UnitRegistry`][] used by ome-types.
ureg: pint.UnitRegistry = pint.UnitRegistry(
    auto_reduce_dimensions=True, on_redefinition="ignore"
)

ureg.define("reference_frame = [_reference_frame]")
ureg.define("@alias grade = gradian")
ureg.define("@alias astronomical_unit = ua")
ureg.define("line = inch / 12")
ureg.define("millitorr = torr / 1000 = mTorr")
ureg.define("@alias torr = Torr")
ureg.define("@alias point = pt")

_UNIT_FIELD = "{}_unit"


def _quantity_property(field_name: str) -> property:
    """Create property that returns a ``pint.Quantity`` combining value and unit."""

    def quantity(self: Any) -> pint.Quantity | None:
        value = getattr(self, field_name)
        if value is None:  # pragma: no cover
            return None

        unit = getattr(self, _UNIT_FIELD.format(field_name))
        return ureg.Quantity(value, unit.value.replace(" ", "_"))

    return property(quantity)


def add_quantity_properties(cls: type[BaseModel]) -> None:
    """Add quantity properties to each field with a corresponding *_unit field.

    Quantity properties allow you to access the value and unit of a field in a single
    X_quantity property, where X is the name of the field.  It returns a pint object.
    """
    _QUANTITY_FIELD = "{}_quantity"
    # for some odd reason, cls.model_fields isn't always ready to go yet at this point
    # only in pydantic2... so use __annotations__ instead
    field_names = set(cls.__annotations__)
    for field in field_names:
        if _UNIT_FIELD.format(field) in field_names:
            setattr(cls, _QUANTITY_FIELD.format(field), _quantity_property(field))
