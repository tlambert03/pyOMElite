from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, Callable

from xsdata.formats.dataclass.filters import Filters
from xsdata.formats.dataclass.generator import DataclassGenerator
from xsdata.utils import text
from xsdata.utils.collections import unique_sequence

if TYPE_CHECKING:
    from xsdata.codegen.models import Attr, Class
    from xsdata.models.config import GeneratorConfig, OutputFormat

text.stop_words.update(("schema", "validate"))


class PydanticBaseGenerator(DataclassGenerator):
    """Python pydantic dataclasses code generator."""

    @classmethod
    def init_filters(cls, config: GeneratorConfig) -> Filters:
        return PydanticBaseFilters(config)


class PydanticBaseFilters(Filters):
    def __init__(self, config: GeneratorConfig):
        super().__init__(config)

    @classmethod
    def build_import_patterns(cls) -> dict[str, dict]:
        patterns = Filters.build_import_patterns()
        patterns.update(
            {"pydantic": {"Field": [" = Field("], "BaseModel": ["BaseModel"]}}
        )
        return {key: patterns[key] for key in sorted(patterns)}

    @classmethod
    def build_class_annotation(cls, fmt: OutputFormat) -> str:
        # remove the @dataclass decorator
        return ""

    def field_definition(
        self, attr: Attr, ns_map: dict, parent_namespace: str | None, parents: list[str]
    ) -> str:
        defn = super().field_definition(attr, ns_map, parent_namespace, parents)
        return defn.replace("field(", "Field(")

    def format_arguments(self, kwargs: dict, indent: int = 0) -> str:
        # called by field_definition
        self.move_restrictions_to_pydantic_field(kwargs)
        return super().format_arguments(kwargs, indent)

    def class_bases(self, obj: Class, class_name: str) -> list[str]:
        # add BaseModel to the class bases
        # FIXME ... need to dedupe superclasses
        bases = super().class_bases(obj, class_name)
        return unique_sequence([*bases, "BaseModel"])

    def move_restrictions_to_pydantic_field(
        self, kwargs: dict, pop: bool = False
    ) -> None:
        """Move metadata from the metadata dict to the pydantic Field kwargs."""
        # XXX: can we pop them?  or does xsdata need them in the metadata dict as well?
        if "metadata" not in kwargs:  # pragma: no cover
            return

        metadata: dict = kwargs["metadata"]
        getitem = metadata.pop if pop else metadata.get
        for from_, to_ in V2_RESTRICTION_MAP.items():
            if from_ in metadata:
                kwargs[to_] = getitem(from_)

        if "metadata" in kwargs:
            kwargs["json_schema_extra"] = kwargs.pop("metadata")

    # note, this method is the same as the base class implementation before it
    # was changed in xsdata v24.  that change breaks private package names... so
    # we're using the old implementation here.
    # https://github.com/tefra/xsdata/issues/948
    def safe_name(
        self, name: str, prefix: str, name_case: Callable, **kwargs: Any
    ) -> str:
        """Sanitize names for safe generation."""
        if not name:
            return self.safe_name(prefix, prefix, name_case, **kwargs)

        if re.match(r"^-\d*\.?\d+$", name):
            return self.safe_name(f"{prefix}_minus_{name}", prefix, name_case, **kwargs)

        slug = text.alnum(name)
        if not slug or not slug[0].isalpha():
            return self.safe_name(f"{prefix}_{name}", prefix, name_case, **kwargs)

        result = name_case(name, **kwargs)
        if text.is_reserved(result):
            return self.safe_name(f"{name}_{prefix}", prefix, name_case, **kwargs)

        return result


V1_RESTRICTION_MAP = {
    "min_occurs": "min_items",  # semantics are different
    "max_occurs": "max_items",  # semantics are different
    "min_exclusive": "gt",
    "min_inclusive": "ge",
    "max_exclusive": "lt",
    "max_inclusive": "le",
    "min_length": "min_length",  # only applies to strings
    "max_length": "max_length",  # only applies to strings
    "pattern": "regex",
    "fraction_digits": "decimal_places",
    "total_digits": "max_digits",
    # --- other restrictions that don't have a direct mapping ---
    # "length": "...",
    # "white_space": "...",
    # "explicit_timezone": "...",
    # "nillable": "...",
    # "sequence": "...",
    # "tokens": "...",
    # "format": "...",
    # "choice": "...",
    # "group": "...",
    # "path": "...",
}
V2_RESTRICTION_MAP = {
    **V1_RESTRICTION_MAP,
    "min_occurs": "min_length",  # semantics are different
    "max_occurs": "max_length",  # semantics are different
    "pattern": "pattern",
}
