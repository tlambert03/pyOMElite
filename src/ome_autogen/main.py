from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from shutil import rmtree
from typing import Any

from xsdata.codegen.writer import CodeWriter
from xsdata.models import config as cfg
from xsdata.utils import text

from ome_autogen import _util
from ome_autogen._util import camel_to_snake
from ome_autogen.generator import OmeGenerator
from ome_autogen.overrides import MIXINS
from ome_autogen.transformer import OMETransformer
from xsdata_pydantic_basemodel.config import GeneratorOutput

# these are normally "reserved" names that we want to allow as field names
ALLOW_RESERVED_NAMES = {"type", "Type", "Union"}
# format key used to register our custom OmeGenerator
OME_FORMAT = "OME"

PYDANTIC_SUPPORT = os.getenv("PYDANTIC_SUPPORT", "both")
RUFF_LINE_LENGTH = 88
RUFF_TARGET_VERSION = "py38"
OUTPUT_PACKAGE = "ome_types._autogenerated.ome_2016_06"
DO_MYPY = os.environ.get("OME_AUTOGEN_MYPY", "0") == "1" or "--mypy" in sys.argv
SRC_PATH = Path(__file__).parent.parent
SCHEMA_FILE = (SRC_PATH / "ome_types" / "ome-2016-06.xsd").absolute()
RUFF_IGNORE: list[str] = [
    "D101",  # Missing docstring in public class
    "D106",  # Missing docstring in public nested class
    "D205",  # 1 blank line required between summary line and description
    "D404",  # First word of the docstring should not be This
    "E501",  # Line too long
    "S105",  # Possible hardcoded password
    "RUF002",  # ambiguous-unicode-character-docstring
]


def get_config(
    package: str, kw_only: bool = True, compound_fields: bool = False
) -> cfg.GeneratorConfig:
    """Return a GeneratorConfig for the OME schema."""
    # ALLOW "type" to be used as a field name
    text.stop_words.difference_update(ALLOW_RESERVED_NAMES)

    # use our own camel_to_snake
    # Our's interprets adjacent capital letters as two words
    # NameCase.SNAKE: 'PositionXUnit' -> 'position_xunit'
    # camel_to_snake: 'PositionXUnit' -> 'position_x_unit'
    cfg.__name_case_func__["snakeCase"] = camel_to_snake

    #  critical to be able to use the format="OME"
    CodeWriter.register_generator(OME_FORMAT, OmeGenerator)

    mixins = []
    for class_name, import_string, prepend in MIXINS:
        mixins.append(
            cfg.GeneratorExtension(
                type=cfg.ExtensionType.CLASS,
                class_name=class_name,
                import_string=import_string,
                prepend=prepend,
            )
        )

    keep_case = cfg.NameConvention(cfg.NameCase.ORIGINAL, "type")
    return cfg.GeneratorConfig(
        output=GeneratorOutput(
            package=package,
            # format.value lets us use our own generator
            # kw_only is important, it makes required fields actually be required
            format=cfg.OutputFormat(value=OME_FORMAT, kw_only=kw_only),
            structure_style=cfg.StructureStyle.CLUSTERS,
            docstring_style=cfg.DocstringStyle.NUMPY,
            compound_fields=cfg.CompoundFields(enabled=compound_fields),
            # whether to create models that work for both pydantic 1 and 2
            pydantic_support=PYDANTIC_SUPPORT,  # type: ignore
        ),
        # Add our mixins
        extensions=cfg.GeneratorExtensions(mixins),
        # Don't convert things like XMLAnnotation to XmlAnnotation
        conventions=cfg.GeneratorConventions(class_name=keep_case),
    )


def build_model(
    output_dir: Path | str = SRC_PATH,
    schema_file: Path | str = SCHEMA_FILE,
    target_package: str = OUTPUT_PACKAGE,
    ruff_ignore: list[str] = RUFF_IGNORE,
    do_formatting: bool = True,
    do_mypy: bool = DO_MYPY,
) -> None:
    """Convert the OME schema to a python model."""
    config = get_config(target_package)
    transformer = OMETransformer(print=False, config=config)

    _print_gray(f"Processing {getattr(schema_file ,'name', schema_file)}...")
    transformer.process_sources([Path(schema_file).resolve().as_uri()])

    package_dir = str(Path(output_dir) / OUTPUT_PACKAGE.replace(".", "/"))
    rmtree(package_dir, ignore_errors=True)
    with _util.cd(output_dir):  # xsdata doesn't support output path
        _print_gray("Writing Files...")
        transformer.process_classes()

    _build_typed_dicts(package_dir)
    if do_formatting:
        _fix_formatting(package_dir, ruff_ignore)

    if do_mypy:
        _check_mypy(package_dir)

    _print_green(f"OME python model created at {OUTPUT_PACKAGE}")


def _fix_formatting(package_dir: str, ruff_ignore: list[str] = RUFF_IGNORE) -> None:
    _print_gray("Running ruff check...")

    ruff_chk = ["ruff", "check", "-q", "--fix", "--unsafe-fixes", package_dir]
    ruff_chk.extend(f"--ignore={ignore}" for ignore in ruff_ignore)
    subprocess.check_call(ruff_chk)  # noqa S

    _print_gray("Running ruff format...")
    ruff_fmt = [
        "ruff",
        "format",
        "-q",
        f"--line-length={RUFF_LINE_LENGTH}",
        f"--target-version={RUFF_TARGET_VERSION}",
    ]
    ruff_fmt.extend([str(x) for x in Path(package_dir).rglob("*.py")])
    subprocess.check_call(ruff_fmt)  # noqa S


def _check_mypy(package_dir: str) -> None:
    _print_gray("Running mypy ...")

    mypy = ["mypy", package_dir, "--strict"]
    try:
        subprocess.check_output(mypy, stderr=subprocess.STDOUT)  # noqa S
    except subprocess.CalledProcessError as e:  # pragma: no cover
        raise RuntimeError(f"mypy errors:\n\n{e.output.decode()}") from e


def _print_gray(text: str) -> None:
    if os.name != "nt":
        # UnicodeEncodeError: 'charmap' codec can't encode character '\u2713'
        text = f"\033[90m\033[1m{text}\033[0m"
    print(text)


def _print_green(text: str) -> None:
    if os.name != "nt":
        # UnicodeEncodeError: 'charmap' codec can't encode character '\u2713'
        text = f"\033[92m\033[1m{text}\033[0m"
    print(text)


KWARGS_MODULE = """
from __future__ import annotations
from typing_extensions import TypeAlias
from typing import Union, List, TypedDict
from datetime import datetime
import ome_types.model as ome

class RefDict(TypedDict):
    id: str
"""


def _build_typed_dicts(package_dir: str) -> None:
    """Create a TypedDict class for each OMEType subclass.

    Useful for passing kwargs to the constructors.

    https://peps.python.org/pep-0692/

    def foo(**kwargs: Unpack[ome.ImageDict]) -> None:
        ...
    """
    # sourcery skip: assign-if-exp, reintroduce-else
    try:
        from pydantic._internal._repr import display_as_type
    except ImportError:
        # don't try to do this on pydantic1
        return
    if PYDANTIC_SUPPORT == "v1":
        return

    from ome_types import model
    from ome_types._mixins._base_type import OMEType

    ome_models = {
        name: obj
        for name, obj in vars(model).items()
        if isinstance(obj, type) and issubclass(obj, OMEType) and obj.__annotations__
    }

    def _disp_type(obj: Any) -> str:
        x = display_as_type(obj).replace("NoneType", "None")
        if "ForwardRef" in x:
            #  replace "List[ForwardRef('Map.M')]" with "List[Map.M]"
            x = re.sub(r"ForwardRef\('([a-zA-Z_.]*)'\)", r"\1", x)
        x = re.sub(r"ome_types\._autogenerated\.ome_2016_06.[^.]+.", "", x)
        return x

    # add TypedDicts for all models
    module = KWARGS_MODULE
    SUFFIX = "Dict"
    CLASS = "class {name}(TypedDict, total=False):\n    {fields}\n\n"
    for cls_name, m in sorted(ome_models.items()):
        if cls_name.endswith("Ref"):
            module += f"{cls_name}: TypeAlias = RefDict\n"
        else:
            _fields = [
                f"{k}: {_disp_type(v.annotation)}"
                # this type ignore indicates something that may break in pydantic 3
                # but for now, it's confusing and I think it's an error
                for k, v in sorted(m.model_fields.items())  # type: ignore
            ]
            if _fields:
                module += CLASS.format(
                    name=f"{m.__name__}{SUFFIX}", fields="\n    ".join(_fields)
                )
            else:
                module += (
                    f"class {m.__name__}{SUFFIX}(TypedDict, total=False):\n    pass\n\n"
                )

    # fix name spaces
    # prefix all remaining capitalized words with ome.
    def _repl(match: re.Match) -> str:
        word = match[1]
        if word in {"None", "True", "False", "Union", "List", "TypedDict", "TypeAlias"}:
            return word
        if word.endswith(SUFFIX):
            return word
        if word in ome_models:
            return word + SUFFIX
        # the rest are enums, they can be passed as strings
        return f"ome.{word} | str"

    module = re.sub(r"\b([A-Z][a-zA-Z_^.]*)\b", _repl, module)
    (Path(package_dir) / "kwargs.py").write_text(module)
