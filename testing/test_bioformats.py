import os
import sys
from pathlib import Path

import pytest

from ome_types import from_bioformats, from_tiff

if os.getenv("CI") and not sys.platform.startswith("linux"):
    pytest.skip("not on linux, skipping bioformats", allow_module_level=True)


def test_bioformats() -> None:
    data = Path(__file__).parent / "data" / "ome.tiff"
    ome = from_bioformats(data)
    ome2 = from_tiff(data)
    # cop out... they read a little differently
    assert ome.uuid == ome2.uuid


def test_bioformats2() -> None:
    # for CI, this should grab a local copy
    data = Path(__file__).parent / "data" / "ome.tiff"
    ome = from_bioformats(data)
    ome2 = from_tiff(data)
    # cop out... they read a little differently
    assert ome.uuid == ome2.uuid
