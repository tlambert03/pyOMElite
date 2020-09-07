import importlib
import sys
from pathlib import Path
import pytest

ome_autogen = pytest.importorskip("ome_autogen")


def test_autogen(tmp_path_factory):
    target_dir = tmp_path_factory.mktemp("test_model")
    xsd = Path(__file__).parent.parent / "src" / "ome_types" / "ome-2016-06.xsd"
    ome_autogen.convert_schema(url=xsd, target_dir=target_dir)
    sys.path.insert(0, str(target_dir.parent))
    assert importlib.import_module(target_dir.name)
    sys.path.pop(0)
