from __future__ import annotations

import io
import operator
import os
import warnings
from contextlib import nullcontext, suppress
from functools import cache
from pathlib import Path
from struct import Struct
from typing import TYPE_CHECKING, Callable, cast, overload

from pydantic import BaseModel
from xsdata.formats.dataclass.parsers.config import ParserConfig

from xsdata_pydantic_basemodel.bindings import (
    SerializerConfig,
    XmlParser,
    XmlSerializer,
)

try:
    from lxml import etree as ET
except ImportError:  # pragma: no cover
    from xml.etree import ElementTree as ET  # type: ignore[no-redef]


if TYPE_CHECKING:
    from collections.abc import Iterable
    from contextlib import AbstractContextManager
    from typing import Any, BinaryIO, Literal, TypedDict
    from xml.etree import ElementTree

    import xmlschema
    from lxml.etree import _XSLTResultTree
    from xsdata.formats.dataclass.parsers.mixins import XmlHandler

    from ome_types._mixins._base_type import OMEType
    from ome_types.model import OME
    from xsdata_pydantic_basemodel.bindings import XmlContext

    AnyElement = ET._Element | ElementTree.Element
    AnyElementTree = ElementTree.ElementTree | ET._ElementTree
    ElementOrTree = AnyElement | AnyElementTree
    TransformationCallable = Callable[[AnyElementTree], AnyElementTree]
    XMLSource = Path | str | bytes | BinaryIO
    FileLike = str | io.BufferedIOBase

    class ParserKwargs(TypedDict, total=False):
        config: ParserConfig
        context: XmlContext
        handler: type[XmlHandler]


__all__ = ["from_tiff", "from_xml", "tiff2xml", "to_dict", "to_xml"]

OME_ROOT = "http://www.openmicroscopy.org/Schemas/OME"
OME_2016_06_URI = f"{OME_ROOT}/2016-06"
OME_2016_06_NS = f"{{{OME_2016_06_URI}}}"
OME_2016_06_XSD = str(Path(__file__).parent / "ome-2016-06.xsd")


def from_xml(
    source: XMLSource,
    *,
    validate: bool | None = None,
    parser: Any = None,
    parser_kwargs: ParserKwargs | None = None,
    transformations: Iterable[TransformationCallable] = (),
    warn_on_schema_update: bool = False,
) -> OME:  #  Not totally true, see note below
    """Generate an OME object from an XML document.

    NOTE: Technically, this can return any ome-types instance, (not just OME) but it's
    by far the most common type that will come out of this function, and the type
    annotation will be more useful to most users. For those who pass in an xml document
    that isn't just a root <OME> tag, they can cast the result to the correct type
    themselves.

    Parameters
    ----------
    source : Path | str | bytes | io.BytesIO,
        Path to an XML file, string or bytes containing XML, or a file-like object.
        If the source is not OME-2016-06 XML, it will be transformed to that namespace
        if possible.
    validate : bool | None
        Whether to validate the XML document against the OME schema.
        If None, validation will be skipped if lxml is not available,
        and will be performed otherwise.
    parser : Any
        Ignored, but kept for backwards compatibility.
    parser_kwargs : ParserKwargs | None
        Passed to the XmlParser constructor. If None, a default parser
        will be used.
    transformations: Iterable[TransformationCallable]
        A sequence of functions that take an ElementTree and return an ElementTree.
        These will be applied sequentially to the XML document before parsing.
        Can be used to apply custom transformations or fixes to the XML document
        before parsing.
    warn_on_schema_update : bool
        Whether to warn if a transformation was applied to bring the document to
        OME-2016-06.

    Returns
    -------
    OME
        The OME object parsed from the XML document. (See NOTE above.)
    """
    if parser is not None:  # pragma: no cover
        warnings.warn(
            "As of version 0.4.0, the parser argument is ignored. "
            "lxml will be used if available in the environment, but you can "
            "drop this keyword argument.",
            DeprecationWarning,
            stacklevel=2,
        )

    if validate:
        xml_2016 = validate_xml(source, warn_on_schema_update=warn_on_schema_update)
    else:
        xml_2016 = ensure_2016(
            source, warn_on_schema_update=warn_on_schema_update, as_tree=True
        )

    for transform in transformations:
        tree_out = transform(xml_2016)
        if tree_out is not None:
            xml_2016 = tree_out
        else:
            warnings.warn("Transformation returned None, skipping", stacklevel=2)

    OME_type = _get_root_ome_type(xml_2016)
    parser = XmlParser(**(parser_kwargs or {}))
    return parser.parse(xml_2016, OME_type)


# ------------------------


def from_tiff(
    path: Path | str | BinaryIO,
    *,
    validate: bool | None = None,
    parser_kwargs: ParserKwargs | None = None,
) -> OME:
    """Generate an OME object from a TIFF file.

    Parameters
    ----------
    path : Path | str | BinaryIO
        Path to a TIFF file or a file-like object.
    validate : bool | None
        Whether to validate the XML document against the OME schema before parsing.
        If None, validation will be skipped if lxml is not available,
        and will be performed otherwise.
    parser_kwargs : ParserKwargs | None
        Passed to the XmlParser constructor. If None, a default parser
        will be used.
    """
    xml = tiff2xml(path)
    return from_xml(xml, validate=validate, parser_kwargs=parser_kwargs)


TIFF_TYPES: dict[bytes, tuple[Struct, Struct, int, Struct]] = {
    b"II*\0": (Struct("<I"), Struct("<H"), 12, Struct("<H")),
    b"MM\0*": (Struct(">I"), Struct(">H"), 12, Struct(">H")),
    b"II+\0": (Struct("<Q"), Struct("<Q"), 20, Struct("<H")),
    b"MM\0+": (Struct(">Q"), Struct(">Q"), 20, Struct(">H")),
}


def _unpack(fh: BinaryIO, strct: Struct) -> int:
    return strct.unpack(fh.read(strct.size))[0]


def tiff2xml(path: Path | str | BinaryIO) -> bytes:
    """Extract the OME-XML from a TIFF file."""
    if hasattr(path, "read"):
        ctx: AbstractContextManager[BinaryIO] = nullcontext(path)  # type: ignore[arg-type]
    else:
        ctx = Path(path).open(mode="rb")

    with ctx as fh:
        head = fh.read(4)
        if head not in TIFF_TYPES:  # pragma: no cover
            raise ValueError(f"{path!r} does not have a recognized TIFF header")

        offset_fmt, tagno_fmt, tagsize, codeformat = TIFF_TYPES[head]
        offset_size = offset_fmt.size
        offset_size_4 = offset_size + 4

        if offset_size == 8:
            fh.seek(4, 1)
        fh.seek(_unpack(fh, offset_fmt))
        for _ in range(_unpack(fh, tagno_fmt)):
            tagstruct = fh.read(tagsize)
            if codeformat.unpack(tagstruct[:2])[0] == 270:
                size = offset_fmt.unpack(tagstruct[4:offset_size_4])[0]
                if size <= offset_size:
                    desc = tagstruct[offset_size_4 : offset_size_4 + size]
                    break
                fh.seek(offset_fmt.unpack(tagstruct[-offset_size:])[0])
                desc = fh.read(size)
                break
        else:  # pragma: no cover
            raise ValueError(f"No OME metadata found in file: {path}")

    if desc[-1] == 0:
        desc = desc[:-1]  # pragma: no cover
    return desc


# ------------------------


def to_dict(source: OME | XMLSource) -> dict[str, Any]:
    """Return a dictionary representation of an OME or XML document.

    Parameters
    ----------
    source : OME | Path | str | bytes | io.BytesIO
        An OME object, or a path to an XML file, or a string or bytes containing XML.

    Returns
    -------
    dict[str, Any]
        A dictionary representation of the OME object or XML document.
    """
    if isinstance(source, BaseModel):
        return source.model_dump(exclude_defaults=True)

    return from_xml(  # type: ignore[return-value]
        source,
        # the class_factory is what prevents class instantiation,
        # simply returning the params instead
        # normally, the class_factory is supposed to return an instance of a,
        # hence the type: ignore
        parser_kwargs={"config": ParserConfig(class_factory=lambda a, b: b)},  # type: ignore
    )


def to_xml(
    obj: OMEType,
    *,
    # exclude_defaults takes precedence over exclude_unset
    # if a value equals the default, it will be excluded
    exclude_defaults: bool = False,
    # exclude_unset will exclude any value that is not explicitly set
    # but will INCLUDE values that are set to their default
    exclude_unset: bool = True,
    indent: int = 2,
    include_namespace: bool | None = None,
    include_schema_location: bool = True,
    canonicalize: bool = False,
    validate: bool = False,
) -> str:
    """Generate an XML document from an OME object.

    Parameters
    ----------
    obj : OMEType
        Instance of an ome-types model class.
    exclude_defaults : bool, optional
        Whether to exclude attributes that are set to their default value,
        by default False.
    exclude_unset : bool, optional
        Whether to exclude attributes that are not explicitly set,
        by default True.
    indent : int, optional
        Number of spaces to indent the XML document, by default 2.
    include_namespace : bool | None, optional
        Whether to include the OME namespace in the root element.  If `None`, will
        be set to the value of `canonicalize`, by default None.
    include_schema_location : bool, optional
        Whether to include the schema location in the root element, by default True.
    canonicalize : bool, optional
        Whether to canonicalize the XML output, by default False.
    validate : bool, optional
        Whether to validate the XML document against the OME schema, after rendering.
        (In most cases, this will be redundant and unnecessary.)

    Returns
    -------
    str
        The XML document as a string.
    """
    # xsdata>=24.2
    if hasattr(SerializerConfig, "indent"):
        indent_kwargs: dict = {"indent": " " * indent}
    else:
        indent_kwargs = {
            "pretty_print": (indent > 0) and not canonicalize,  # canonicalize does it
            "pretty_print_indent": " " * indent,
        }
    config = SerializerConfig(
        **indent_kwargs,
        xml_declaration=False,
        ignore_default_attributes=exclude_defaults,
        ignore_unset_attributes=exclude_unset,
        attribute_sort_key=operator.attrgetter("name") if canonicalize else None,
    )
    if include_schema_location:
        config.schema_location = f"{OME_2016_06_URI} {OME_2016_06_URI}/ome.xsd"

    serializer = XmlSerializer(config=config)
    if include_namespace is None:
        include_namespace = canonicalize

    if exclude_unset:
        # if we're excluding unset attributes, we need to be very careful that the
        # __fields_set__ attribute is accurate, otherwise we'll exclude attributes
        # this is tricky for things like mutable sequences that pydantic doesn't
        # know about. this method recurses the object and updates the __fields_set__
        # attribute if the field is not equal to its default value
        obj._update_set_fields()

    ns_map = {"ome" if include_namespace else None: OME_2016_06_URI}
    xml = serializer.render(obj, ns_map=ns_map)

    if canonicalize:
        xml = _canonicalize(xml, indent=" " * indent)
    if validate:
        validate_xml(xml)
    return xml


def _canonicalize(xml: str, indent: str) -> str:
    from xml.dom import minidom

    xml_out = ET.canonicalize(xml, strip_text=True)
    return minidom.parseString(xml_out).toprettyxml(indent=indent)


# ------------------------


class ValidationError(ValueError): ...


def validate_xml(
    xml: XMLSource,
    schema: Path | str | None = None,
    *,
    warn_on_schema_update: bool = True,
) -> AnyElementTree:
    """Validate XML against an XML Schema.

    By default, will validate against the OME 2016-06 schema.
    """
    with suppress(ImportError):
        return validate_xml_with_lxml(xml, schema, warn_on_schema_update)

    with suppress(ImportError):  # pragma: no cover
        return validate_xml_with_xmlschema(xml, schema, warn_on_schema_update)

    raise ImportError(  # pragma: no cover
        "Validation requires either `lxml` or `xmlschema`. "
        "Please pip install one of them."
    ) from None


def validate_xml_with_lxml(
    xml: XMLSource, schema: Path | str | None = None, warn_on_schema_update: bool = True
) -> AnyElementTree:
    """Validate XML against an XML Schema using lxml."""
    from lxml import etree

    tree = ensure_2016(xml, warn_on_schema_update=warn_on_schema_update, as_tree=True)
    xmlschema = etree.XMLSchema(etree.parse(schema or OME_2016_06_XSD))

    if not xmlschema.validate(cast("ET._ElementTree", tree)):
        msg = f"Validation of {str(xml)[:20]!r} failed:"
        for error in xmlschema.error_log:
            msg += f"\n  - line {error.line}: {error.message}"
        raise ValidationError(msg)
    return tree


def validate_xml_with_xmlschema(
    xml: XMLSource, schema: Path | str | None = None, warn_on_schema_update: bool = True
) -> AnyElementTree:
    """Validate XML against an XML Schema using xmlschema."""
    from xmlschema.exceptions import XMLSchemaException

    tree = ensure_2016(xml, warn_on_schema_update=warn_on_schema_update, as_tree=True)
    xmlschema = _get_XMLSchema(schema or OME_2016_06_XSD)
    try:
        xmlschema.validate(tree)  # type: ignore[arg-type]
    except XMLSchemaException as e:
        raise ValidationError(str(e)) from None
    return tree


@cache
def _get_XMLSchema(schema: Path | str) -> xmlschema.XMLSchema:
    import xmlschema

    xml_schema = xmlschema.XMLSchema(schema)
    # FIXME Hack to work around xmlschema poor support for keyrefs to
    # substitution groups
    ls_sgs = xml_schema.maps.substitution_groups[f"{OME_2016_06_NS}LightSourceGroup"]
    ls_id_maps = xml_schema.maps.identities[f"{OME_2016_06_NS}LightSourceIDKey"]
    ls_id_maps.elements = {e: None for e in ls_sgs}
    return xml_schema


# ------------------------

TRANSFORMS_PATH = Path(__file__).parent / "transforms"
TRANSFORMS = {
    f"{OME_ROOT}/{p.name.split('-to')[0]}": p for p in TRANSFORMS_PATH.glob("*.xsl")
}


@overload
def ensure_2016(
    source: XMLSource, *, warn_on_schema_update: bool = ..., as_tree: Literal[True]
) -> AnyElementTree: ...


@overload
def ensure_2016(
    source: XMLSource,
    *,
    warn_on_schema_update: bool = ...,
    as_tree: Literal[False] = ...,
) -> FileLike: ...


def ensure_2016(
    source: XMLSource, *, warn_on_schema_update: bool = False, as_tree: bool = False
) -> FileLike | AnyElementTree:
    """Ensure source is OME-2016-06 XML.

    If the source is not OME-2016-06 XML, it will be transformed sequentially using
    XSLT transforms in the `transforms` directory, until it is in the 2016-06 namespace.
    NOTE: this requires lxml to be installed and will raise an ImportError if it is not.

    Parameters
    ----------
    source : Path | str | bytes | io.BytesIO
        Path to an XML file, string or bytes containing XML, or a file-like object.
    warn_on_schema_update : bool
        Whether to warn if a transformation was applied to bring the document to
        OME-2016-06.
    as_tree : bool
        Whether to return an ElementTree or a FileLike object.

    Returns
    -------
    FileLike | AnyElementTree
        If `as_tree` is `True`, an ElementTree, otherwise a FileLike object representing
        transformed OME 2016 XML.


    Raises
    ------
    ValueError
        If the source is an unrecognized XML namespace.
    ImportError
        If lxml is not installed and a transformation is required.
    """
    normed_source = _normalize(source)
    try:
        ns_in = _get_ns_file(normed_source)
    except Exception as e:
        raise ValueError(f"Could not parse XML from {source!r}") from e

    # catch rare case of OME-XML with lowercase ome in namespace
    if "Schemas/ome/" in ns_in:
        normed_source = _capitalize_ome(normed_source)
        ns_in = _get_ns_file(normed_source)

    if hasattr(normed_source, "seek"):
        normed_source.seek(0)

    if ns_in == OME_2016_06_URI:
        if as_tree:
            return ET.parse(normed_source)
        return normed_source

    if ns_in in TRANSFORMS:
        tree = ET.parse(normed_source)
        ns = ns_in
        while ns in TRANSFORMS:
            tree = _apply_xslt(tree, TRANSFORMS[ns])
            ns = _get_ns_elem(tree)
        if warn_on_schema_update:
            warnings.warn(
                f"Transformed source from {ns_in!r} to {OME_2016_06_URI!r}",
                stacklevel=2,
            )

        return tree if as_tree else io.BytesIO(ET.tostring(tree, encoding="utf-8"))

    raise ValueError(f"Unsupported document namespace {ns_in!r}")


def _capitalize_ome(source: FileLike) -> FileLike:
    """Fix OME namespace capitalization errors."""
    if hasattr(source, "read") and hasattr(source, "seek"):
        source.seek(0)
        data = source.read()
    else:
        with open(source, "rb") as fh:
            data = fh.read()

    io_out = io.BytesIO(data.replace(b"Schemas/ome/", b"Schemas/OME/"))
    io_out.seek(0)
    return io_out


def _normalize(source: XMLSource) -> FileLike:
    """Normalize the input to a BytesIO object, or a filepath.

    Parameters
    ----------
    source : Path | str | bytes | io.BytesIO
        Path to an XML file, string or bytes containing XML, or a file-like object.

    Returns
    -------
    FileLike
        A BytesIO object, or a filepath.
    """
    if isinstance(source, Path):
        return str(source.resolve())
    elif isinstance(source, str):
        if os.path.isfile(source):
            return source
        return io.BytesIO(source.encode())
    elif isinstance(source, bytes):
        return io.BytesIO(source)
    elif isinstance(source, io.BufferedIOBase):
        return source

    if hasattr(source, "mode") and "b" not in source.mode:
        raise TypeError("File must be opened in binary mode")
    raise TypeError(f"Unsupported source type {type(source)!r}")


def _apply_xslt(root: ET._ElementTree, xslt_path: str | Path) -> _XSLTResultTree:
    """Apply an XSLT transform to an element or element tree."""
    try:
        from lxml import etree
    except ImportError:  # pragma: no cover
        ns = _get_ns_elem(root)
        raise ImportError(
            f"This documented is using an outdated schema ({ns!r}). "
            "But lxml is required to update older schemas to OME-2016. "
            "Please run `pip install lxml`"
        ) from None

    # Create a transformer object
    transformer = etree.XSLT(ET.parse(xslt_path))
    return transformer(root)


# ------------------------


def _get_ns_elem(elem: ET._Element | AnyElementTree) -> str:
    """Get namespace from an element or element tree."""
    root = elem.getroot() if hasattr(elem, "getroot") else elem
    # return root.nsmap[root.prefix]  this only works for lxml
    return str(root.tag).split("}", 1)[0].lstrip("{")


def _get_ns_file(source: FileLike) -> str:
    """Get namespace from a file or file-like object."""
    if hasattr(source, "seek"):
        source.seek(0)
    _, root = next(ET.iterparse(source, events=("start",)))
    return _get_ns_elem(root)  # type: ignore[arg-type]


def _get_root_ome_type(xml: FileLike | AnyElementTree) -> type[OMEType]:
    """Resolve a ome_types.model class for the root element of an OME XML document."""
    from ome_types import model

    if hasattr(xml, "getroot"):
        root = xml.getroot()
    else:
        if hasattr(xml, "seek"):
            xml.seek(0)
        _, root = next(ET.iterparse(xml, events=("start",)))
    localname = str(root.tag).rsplit("}", 1)[-1]

    if hasattr(xml, "seek"):
        xml.seek(0)
    try:
        return getattr(model, localname)
    except AttributeError:
        raise ValueError(f"Unknown root element {localname!r}") from None
