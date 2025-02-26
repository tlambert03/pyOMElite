from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable
from xml.etree.ElementTree import QName

from xsdata.formats.dataclass import context, parsers, serializers
from xsdata.formats.dataclass.serializers import config
from xsdata.formats.dataclass.serializers.mixins import XmlWriterEvent
from xsdata.models.enums import QNames
from xsdata.utils import collections, namespaces
from xsdata.utils.constants import EMPTY_MAP, return_input

if TYPE_CHECKING:
    from collections.abc import Generator, Iterator

    from pydantic import BaseModel
    from xsdata.formats.dataclass.models.elements import XmlMeta


class XmlContext(context.XmlContext):
    """Pydantic BaseModel ready xml context instance."""

    def __init__(
        self,
        element_name_generator: Callable = return_input,
        attribute_name_generator: Callable = return_input,
    ):
        super().__init__(
            element_name_generator, attribute_name_generator, "pydantic-basemodel"
        )


class SerializerConfig(config.SerializerConfig):
    # here to add `ignore_unset_attributes` support to XmlSerializer
    __slots__ = (
        *getattr(config.SerializerConfig, "__slots__", ()),
        "ignore_unset_attributes",
        "attribute_sort_key",
    )

    def __init__(self, **kwargs: Any) -> None:
        self.ignore_unset_attributes = kwargs.pop("ignore_unset_attributes", False)
        self.attribute_sort_key = kwargs.pop("attribute_sort_key", None)
        super().__init__(**kwargs)


@dataclass
class XmlParser(parsers.XmlParser):
    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class XmlSerializer(serializers.XmlSerializer):
    context: XmlContext = field(default_factory=XmlContext)

    # overriding so we can pass the args we want to next_attribute
    # and so that we can skip unset values
    def write_dataclass(
        self,
        obj: BaseModel,
        namespace: str | None = None,
        qname: str | None = None,
        nillable: bool = False,
        xsi_type: str | None = None,
    ) -> Generator:
        """
        Produce an events stream from a dataclass.

        Optionally override the qualified name and the xsi properties
        type and nil.
        """
        meta = self.context.build(
            obj.__class__, namespace, globalns=self.config.globalns
        )
        qname = qname or meta.qname
        nillable = nillable or meta.nillable
        namespace, tag = namespaces.split_qname(qname)

        yield XmlWriterEvent.START, qname

        # XXX: reason 1 for overriding.
        ignore_unset = getattr(self.config, "ignore_unset_attributes", False)
        for key, value in self.next_attribute(
            obj,
            meta,
            nillable,
            xsi_type,
            self.config.ignore_default_attributes,
            ignore_unset,
            getattr(self.config, "attribute_sort_key", None),
        ):
            yield XmlWriterEvent.ATTR, key, value

        for var, value in self.next_value(obj, meta):
            # XXX: reason 2 for overriding.
            if ignore_unset and var.name not in obj.model_fields_set:
                continue
            yield from self.write_value(value, var, namespace)

        yield XmlWriterEvent.END, qname

    # overriding so we can implement support for `ignore_unset_attributes`
    # and so that we can sort attributes as we want
    @classmethod
    def next_attribute(
        cls,
        obj: BaseModel,
        meta: XmlMeta,
        nillable: bool,
        xsi_type: str | None,
        ignore_optionals: bool,
        ignore_unset: bool = False,
        attribute_sort_key: Callable | None = None,
    ) -> Iterator[tuple[str, Any]]:
        """
        Return the attribute variables with their object values if set and not
        empty iterables.

        :param obj: Input object
        :param meta: Object metadata
        :param nillable: Is model nillable
        :param xsi_type: The true xsi:type of the object
        :param ignore_optionals: Skip optional attributes with default
            value
        :return:
        """

        set_fields = obj.model_fields_set if ignore_unset else set()
        vars_ = meta.get_attribute_vars()
        if attribute_sort_key is not None:
            vars_ = sorted(meta.get_attribute_vars(), key=attribute_sort_key)

        # ^^^ new

        for var in vars_:
            if var.is_attribute:
                value = getattr(obj, var.name)
                if (
                    value is None
                    or (collections.is_array(value) and not value)
                    or (ignore_optionals and var.is_optional(value))
                    or (ignore_unset and var.name not in set_fields)  # new
                ):
                    continue
                yield var.qname, cls.encode(value, var)
            else:
                yield from getattr(obj, var.name, EMPTY_MAP).items()

        if xsi_type:
            yield QNames.XSI_TYPE, QName(xsi_type)

        if nillable:
            yield QNames.XSI_NIL, "true"


@dataclass
class JsonParser(parsers.JsonParser):
    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class JsonSerializer(serializers.JsonSerializer):
    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class UserXmlParser(parsers.UserXmlParser):
    context: XmlContext = field(default_factory=XmlContext)
