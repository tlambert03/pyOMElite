from typing import Iterator, Sequence, Union, overload

from ome_types._mixins._base_type import OMEType
from ome_types.model.ome_2016_06.annotation import Annotation


class StructuredAnnotationsMixin(OMEType, Sequence[Annotation]):
    def _iter_annotations(self) -> Iterator[Annotation]:
        for x in self.__fields__.values():
            if issubclass(x.type_, Annotation):
                yield from getattr(self, x.name)

    @overload
    def __getitem__(self, index: int) -> Annotation:
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[Annotation]:
        ...

    def __getitem__(
        self, key: Union[int, slice]
    ) -> Union[Annotation, Sequence[Annotation]]:
        return list(self._iter_annotations())[key]

    def __len__(self) -> int:
        return len(list(self._iter_annotations()))

    def __iter__(self) -> Iterator[Annotation]:  # type: ignore[override]
        return self._iter_annotations()

    def append(self, value: Annotation) -> None:
        if not isinstance(value, Annotation):
            raise TypeError(f"Value must be a StructuredAnnotation, got {type(value)}")
        for field_name, field in self.__fields__.items():
            if isinstance(value, field.type_):
                getattr(self, field_name).append(value)
                return
