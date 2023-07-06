from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from shutil import rmtree

from ome_autogen import _util
from ome_autogen._config import get_config
from ome_autogen._transformer import OMETransformer

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
]


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

    if do_formatting:
        _fix_formatting(package_dir, ruff_ignore)

    if do_mypy:
        _check_mypy(package_dir)

    _print_green(f"OME python model created at {OUTPUT_PACKAGE}")


def _fix_formatting(package_dir: str, ruff_ignore: list[str] = RUFF_IGNORE) -> None:
    _print_gray("Running black and ruff ...")

    black = ["black", package_dir, "-q", "--line-length=88"]
    subprocess.check_call(black)  # noqa S

    ruff = ["ruff", "-q", "--fix", package_dir]
    ruff.extend(f"--ignore={ignore}" for ignore in ruff_ignore)
    subprocess.check_call(ruff)  # noqa S


def _check_mypy(package_dir: str) -> None:
    _print_gray("Running mypy ...")

    mypy = ["mypy", package_dir, "--strict"]
    try:
        subprocess.check_output(mypy, stderr=subprocess.STDOUT)  # noqa S
    except subprocess.CalledProcessError as e:
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
