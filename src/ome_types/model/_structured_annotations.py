from contextlib import suppress
from typing import List

from pydantic import Field, ValidationError, validator

from ome_types._mixins._base_type import OMEType
from ome_types.model.ome_2016_06.annotation import Annotation
from ome_types.model.ome_2016_06.boolean_annotation import BooleanAnnotation
from ome_types.model.ome_2016_06.comment_annotation import CommentAnnotation
from ome_types.model.ome_2016_06.double_annotation import DoubleAnnotation
from ome_types.model.ome_2016_06.file_annotation import FileAnnotation
from ome_types.model.ome_2016_06.list_annotation import ListAnnotation
from ome_types.model.ome_2016_06.long_annotation import LongAnnotation
from ome_types.model.ome_2016_06.map_annotation import MapAnnotation
from ome_types.model.ome_2016_06.tag_annotation import TagAnnotation
from ome_types.model.ome_2016_06.term_annotation import TermAnnotation
from ome_types.model.ome_2016_06.timestamp_annotation import TimestampAnnotation
from ome_types.model.ome_2016_06.xml_annotation import XMLAnnotation

from ._user_sequence import UserSequence

AnotationCls = (
    BooleanAnnotation,
    CommentAnnotation,
    DoubleAnnotation,
    FileAnnotation,
    ListAnnotation,
    LongAnnotation,
    MapAnnotation,
    TagAnnotation,
    TermAnnotation,
    TimestampAnnotation,
    XMLAnnotation,
)


class StructuredAnnotations(OMEType, UserSequence[Annotation]):  # type: ignore[misc]
    # NOTE: in reality, this is List[Annotation]... but
    # for some reason that messes up xsdata data binding
    __root__: List[object] = Field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": tuple(
                {"name": cls.__name__, "type": cls} for cls in AnotationCls
            ),
        },
    )

    @validator("__root__", each_item=True)
    def _validate_root(cls, v: Annotation) -> Annotation:
        if isinstance(v, AnotationCls):
            return v
        if isinstance(v, dict):
            for cls_ in AnotationCls:
                with suppress(ValidationError):
                    return cls_(**v)
        raise ValueError(f"Invalid StructuredAnnotation: {v}")
