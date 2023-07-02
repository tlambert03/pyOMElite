from contextlib import suppress
from typing import List, Type, Union

from pydantic import Field, ValidationError, validator

from ome_types._mixins._base_type import OMEType
from ome_types.model.ome_2016_06.ellipse import Ellipse
from ome_types.model.ome_2016_06.label import Label
from ome_types.model.ome_2016_06.line import Line
from ome_types.model.ome_2016_06.mask import Mask
from ome_types.model.ome_2016_06.point import Point
from ome_types.model.ome_2016_06.polygon import Polygon
from ome_types.model.ome_2016_06.polyline import Polyline
from ome_types.model.ome_2016_06.rectangle import Rectangle

from ._user_sequence import UserSequence

ShapeType = Union[Rectangle, Mask, Point, Ellipse, Line, Polyline, Polygon, Label]
_KINDS: dict[str, Type[ShapeType]] = {
    "rectangle": Rectangle,
    "mask": Mask,
    "point": Point,
    "ellipse": Ellipse,
    "line": Line,
    "polyline": Polyline,
    "polygon": Polygon,
    "label": Label,
}

_ShapeCls = tuple(_KINDS.values())


class ShapeUnion(OMEType, UserSequence[ShapeType]):  # type: ignore[misc]
    # NOTE: in reality, this is List[ShapeGroupType]... but
    # for some reason that messes up xsdata data binding
    __root__: List[object] = Field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": tuple(
                {"name": kind.title(), "type": cls} for kind, cls in _KINDS.items()
            ),
        },
    )

    @validator("__root__", each_item=True)
    def _validate_root(cls, v: ShapeType) -> ShapeType:
        if isinstance(v, _ShapeCls):
            return v
        if isinstance(v, dict):
            # NOTE: this is here to preserve the v1 behavior of passing a dict like
            # {"kind": "label", "x": 0, "y": 0}
            # to create a label rather than a point
            if "kind" in v:
                kind = v.pop("kind").lower()
                return _KINDS[kind](**v)

            for cls_ in _ShapeCls:
                with suppress(ValidationError):
                    return cls_(**v)
        raise ValueError(f"Invalid shape: {v}")
