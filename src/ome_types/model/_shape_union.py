from contextlib import suppress
from typing import Dict, Iterator, List, Sequence, Type, Union

import pydantic.version
from pydantic import Field, ValidationError, validator

from ome_types._autogenerated.ome_2016_06.ellipse import Ellipse
from ome_types._autogenerated.ome_2016_06.label import Label
from ome_types._autogenerated.ome_2016_06.line import Line
from ome_types._autogenerated.ome_2016_06.mask import Mask
from ome_types._autogenerated.ome_2016_06.point import Point
from ome_types._autogenerated.ome_2016_06.polygon import Polygon
from ome_types._autogenerated.ome_2016_06.polyline import Polyline
from ome_types._autogenerated.ome_2016_06.rectangle import Rectangle
from ome_types._mixins._base_type import OMEType
from ome_types.model._user_sequence import UserSequence

ShapeType = Union[Rectangle, Mask, Point, Ellipse, Line, Polyline, Polygon, Label]
_KINDS: Dict[str, Type[ShapeType]] = {
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

PYDANTIC2 = pydantic.version.VERSION.startswith("2")

if PYDANTIC2:
    from pydantic import RootModel, field_validator

    class ShapeUnion(OMEType, RootModel, UserSequence[ShapeType]):  # type: ignore[misc]
        """A mutable sequence of [`ome_types.model.Shape`][].

        Members of this sequence must be one of the following types:

        - [`ome_types.model.Rectangle`][]
        - [`ome_types.model.Mask`][]
        - [`ome_types.model.Point`][]
        - [`ome_types.model.Ellipse`][]
        - [`ome_types.model.Line`][]
        - [`ome_types.model.Polyline`][]
        - [`ome_types.model.Polygon`][]
        - [`ome_types.model.Label`][]
        """

        # NOTE: in reality, this is List[ShapeGroupType]... but
        # for some reason that messes up xsdata data binding
        root: List[object] = Field(
            default_factory=list,
            json_schema_extra={
                "type": "Elements",
                "choices": tuple(  # type: ignore[dict-item]
                    {"name": kind.title(), "type": cls} for kind, cls in _KINDS.items()
                ),
            },
        )

        @field_validator("root")
        def _validate_root(cls, value: ShapeType) -> ShapeType:
            if not isinstance(value, Sequence):  # pragma: no cover
                raise ValueError(f"Value must be a sequence, not {type(value)}")

            items = []
            for v in value:
                if isinstance(v, _ShapeCls):
                    items.append(v)
                elif isinstance(v, dict):
                    # NOTE: this is here to preserve the v1 behavior of passing a dict
                    # like {"kind": "label", "x": 0, "y": 0}
                    # to create a label rather than a point
                    if "kind" in v:
                        kind = v.pop("kind").lower()
                        items.append(_KINDS[kind](**v))
                    else:
                        for cls_ in _ShapeCls:
                            with suppress(ValidationError):
                                items.append(cls_(warn_extra=False, **v))
                                break
                else:  # pragma: no cover
                    raise ValueError(f"Invalid shape: {v}")  # pragma: no cover
            return items

        def __repr__(self) -> str:
            return f"{self.__class__.__name__}({self.root!r})"

        # overriding BaseModel.__iter__ to behave more like a real Sequence
        def __iter__(self) -> Iterator[ShapeType]:  # type: ignore[override]
            yield from self.root  # type: ignore[misc]  # see NOTE above

        def __eq__(self, _value: object) -> bool:
            return _value == self.root

else:

    class ShapeUnion(OMEType, UserSequence[ShapeType]):  # type: ignore
        """A mutable sequence of [`ome_types.model.Shape`][].

        Members of this sequence must be one of the following types:

        - [`ome_types.model.Rectangle`][]
        - [`ome_types.model.Mask`][]
        - [`ome_types.model.Point`][]
        - [`ome_types.model.Ellipse`][]
        - [`ome_types.model.Line`][]
        - [`ome_types.model.Polyline`][]
        - [`ome_types.model.Polygon`][]
        - [`ome_types.model.Label`][]
        """

        # NOTE: in reality, this is List[ShapeGroupType]... but
        # for some reason that messes up xsdata data binding
        __root__: List[object] = Field(
            default_factory=list,
            metadata={  # type: ignore[call-arg]
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
                        return cls_(warn_extra=False, **v)
            raise ValueError(f"Invalid shape: {v}")  # pragma: no cover

        def __repr__(self) -> str:
            return f"{self.__class__.__name__}({self.__root__!r})"

        # overriding BaseModel.__iter__ to behave more like a real Sequence
        def __iter__(self) -> Iterator[ShapeType]:  # type: ignore[override]
            yield from self.__root__  # type: ignore[misc]  # see NOTE above

        def __eq__(self, _value: object) -> bool:
            return _value == self.__root__
