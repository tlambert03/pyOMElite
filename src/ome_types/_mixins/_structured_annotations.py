import itertools
from typing import Generic, Iterator, TypeVar, Union, cast, no_type_check

# for circular import reasons...
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

T = TypeVar("T")


class CollectionMixin(Generic[T]):
    """Mixin to be used for classes that behave like collections.

    Notably: ShapeUnion and StructuredAnnotations.
    All the fields in these types list[SomeType], and they collectively behave like
    a list with the union of all field types.
    """

    @no_type_check
    def __iter__(self) -> Iterator[T]:
        return itertools.chain(*(getattr(self, f) for f in self.model_fields))

    def __len__(self) -> int:
        return sum(1 for _ in self)

    def append(self, item: T) -> None:
        """Append an item to the appropriate field list."""
        cast(list, getattr(self, self._field_name(item))).append(item)

    def remove(self, item: T) -> None:
        """Remove an item from the appropriate field list."""
        cast(list, getattr(self, self._field_name(item))).remove(item)

    # This one is a bit hacky... perhaps deprecate and remove
    def __getitem__(self, i: int) -> T:
        # return the ith item in the __iter__ sequence
        return next(itertools.islice(self, i, None))

    # perhaps deprecate and remove
    def __eq__(self, _value: object) -> bool:
        if isinstance(_value, list):
            return list(self) == _value
        return super().__eq__(_value)

    @classmethod
    def _field_name(cls, item: T) -> str:
        """Return the name of the field that should contain the given item.

        Must be implemented by subclasses.
        """
        raise NotImplementedError()  # pragma: no cover


# ------------------------ StructuredAnnotations ------------------------

AnnotationType = Union[
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
]
# get_args wasn't available until Python 3.8
AnnotationInstances = AnnotationType.__args__  # type: ignore


class StructuredAnnotationsMixin(CollectionMixin[AnnotationType]):
    ...

    @classmethod
    def _field_name(cls, item: T) -> str:
        if not isinstance(item, AnnotationInstances):
            raise TypeError(  # pragma: no cover
                f"Expected an instance of {AnnotationInstances}, got {item!r}"
            )
        # where 10 is the length of "Annotation"
        return item.__class__.__name__[:-10].lower() + "_annotations"
