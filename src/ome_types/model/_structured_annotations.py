from contextlib import suppress
from typing import Iterator, List

from pydantic import Field, ValidationError, validator

from ome_types._autogenerated.ome_2016_06.annotation import Annotation
from ome_types._autogenerated.ome_2016_06.boolean_annotation import BooleanAnnotation
from ome_types._autogenerated.ome_2016_06.comment_annotation import CommentAnnotation
from ome_types._autogenerated.ome_2016_06.double_annotation import DoubleAnnotation
from ome_types._autogenerated.ome_2016_06.file_annotation import FileAnnotation
from ome_types._autogenerated.ome_2016_06.list_annotation import ListAnnotation
from ome_types._autogenerated.ome_2016_06.long_annotation import LongAnnotation
from ome_types._autogenerated.ome_2016_06.map_annotation import MapAnnotation
from ome_types._autogenerated.ome_2016_06.tag_annotation import TagAnnotation
from ome_types._autogenerated.ome_2016_06.term_annotation import TermAnnotation
from ome_types._autogenerated.ome_2016_06.timestamp_annotation import (
    TimestampAnnotation,
)
from ome_types._autogenerated.ome_2016_06.xml_annotation import XMLAnnotation
from ome_types._mixins._base_type import OMEType
from ome_types.model._user_sequence import UserSequence

AnnotationTypes = (
    XMLAnnotation,
    FileAnnotation,
    ListAnnotation,
    LongAnnotation,
    DoubleAnnotation,
    CommentAnnotation,
    BooleanAnnotation,
    TimestampAnnotation,
    TagAnnotation,
    TermAnnotation,
    MapAnnotation,
)


class StructuredAnnotationList(OMEType, UserSequence[Annotation]):  # type: ignore[misc]
    """A mutable sequence of [`ome_types.model.Annotation`][].

    Members of this sequence must be one of the following types:

    - [`ome_types.model.XMLAnnotation`][]
    - [`ome_types.model.FileAnnotation`][]
    - [`ome_types.model.ListAnnotation`][]
    - [`ome_types.model.LongAnnotation`][]
    - [`ome_types.model.DoubleAnnotation`][]
    - [`ome_types.model.CommentAnnotation`][]
    - [`ome_types.model.BooleanAnnotation`][]
    - [`ome_types.model.TimestampAnnotation`][]
    - [`ome_types.model.TagAnnotation`][]
    - [`ome_types.model.TermAnnotation`][]
    - [`ome_types.model.MapAnnotation`][]
    """

    # NOTE: in reality, this is List[StructuredAnnotationTypes]... but
    # for some reason that messes up xsdata data binding
    __root__: List[object] = Field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": tuple(
                {"name": cls.__name__, "type": cls} for cls in AnnotationTypes
            ),
        },
    )

    @validator("__root__", each_item=True)
    def _validate_root(cls, v: Annotation) -> Annotation:
        if isinstance(v, AnnotationTypes):
            return v
        if isinstance(v, dict):
            for cls_ in AnnotationTypes:
                with suppress(ValidationError):
                    return cls_(**v)
        raise ValueError(f"Invalid Annotation: {v} of type {type(v)}")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__root__!r})"

    # overriding BaseModel.__iter__ to behave more like a real Sequence
    def __iter__(self) -> Iterator[Annotation]:  # type: ignore[override]
        yield from self.__root__  # type: ignore[misc]  # see NOTE above

    def __eq__(self, _value: object) -> bool:
        return _value == self.__root__
