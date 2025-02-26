import datetime
import warnings
from typing import Any

from xsdata.formats.converter import Converter, converter
from xsdata.models.datatype import XmlDateTime

from ome_types.model._color import Color


class DateTimeConverter(Converter):
    def serialize(self, value: datetime.datetime, **kwargs: Any) -> str:
        return str(XmlDateTime.from_datetime(value))

    def deserialize(self, value: Any, **kwargs: Any) -> datetime.datetime:
        xmldt = XmlDateTime.from_string(value)
        try:
            return xmldt.to_datetime()
        except ValueError as e:
            msg = f"Invalid datetime: {value!r} {e}."
            if xmldt.year <= 0:
                msg += "(BC dates are not supported)"
            warnings.warn(msg, stacklevel=2)
            return datetime.datetime(1, 1, 1)


class ColorConverter(Converter):
    def serialize(self, value: Color, **kwargs: Any) -> str:
        return str(value.as_int32())

    def deserialize(self, value: Any, **kwargs: Any) -> Color:
        return Color(value)


def register_converters() -> None:
    converter.register_converter(Color, ColorConverter())
    converter.register_converter(datetime.datetime, DateTimeConverter())
