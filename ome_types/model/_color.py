from contextlib import suppress
from typing import Union

from ome_types._vendor import Color as _Color

__all__ = ["Color"]

RGBA = tuple[int, int, int, float]
ColorType = Union[tuple[int, int, int], RGBA, str, int]


class Color(_Color):
    """A Pydantic Color subclass that converts to and from OME int32 types."""

    def __init__(self, val: ColorType = -1) -> None:
        with suppress(ValueError, TypeError):
            val = self._int2tuple(int(val))  # type: ignore
        super().__init__(val)  # type: ignore [arg-type]

    @classmethod
    def _int2tuple(cls, val: int) -> RGBA:
        return (val >> 24 & 255, val >> 16 & 255, val >> 8 & 255, (val & 255) / 255)

    def as_int32(self) -> int:
        """Convert to an int32, with alpha in the least significant byte."""
        r, g, b, *a = self.as_rgb_tuple()
        v = r << 24 | g << 16 | b << 8 | int((a[0] if a else 1) * 255)
        if v < 2**32 // 2:
            return v
        return v - 2**32

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Color):
            return self.as_int32() == o.as_int32()
        return NotImplemented  # pragma: no cover

    def __int__(self) -> int:
        return self.as_int32()
