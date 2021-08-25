"""Utilities for getting loci_tools.jar, and reading metadata using bioformats."""
import io
import os
import urllib.request
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING, Iterator, Union

logger = getLogger(__name__)

if TYPE_CHECKING:
    import jpype


def _gen_jar_locations() -> Iterator[Path]:
    """
    Generator that yields optional locations of loci_tools.jar.
    The precedence order is (highest priority first):
    1. ome-types package location
    2. PROGRAMDATA/ome-types/loci_tools.jar
    3. LOCALAPPDATA/ome-types/loci_tools.jar
    4. APPDATA/ome-types/loci_tools.jar
    5. /etc/loci_tools.jar
    6. ~/.config/ome-types/loci_tools.jar
    """
    yield Path(__file__).parent
    if "PROGRAMDATA" in os.environ:
        yield Path(os.environ["PROGRAMDATA"]) / "ome-types"
    if "LOCALAPPDATA" in os.environ:
        yield Path(os.environ["LOCALAPPDATA"]) / "ome-types"
    if "APPDATA" in os.environ:
        yield Path(os.environ["APPDATA"]) / "ome-types"
    yield Path("/etc")
    yield Path(os.path.expanduser("~")) / ".config" / "ome-types"


def _get_writable_location() -> Path:
    for loc in _gen_jar_locations():
        # check if dir exists and has write access:
        if loc.exists() and os.access(str(loc), os.W_OK):
            return loc
        # if directory is ome-types and it does not exist, so make it (if allowed)
        if loc.name == "ome-types" and os.access(loc.parent, os.W_OK):
            loc.mkdir(exist_ok=True)
            return loc

    locs = "\n".join(str(x) for x in _gen_jar_locations())
    raise IOError(
        "No writeable location found. In order to use the "
        "Bioformats reader, please download "
        "loci_tools.jar to the ome-types program folder or one of "
        f"the following locations:\n{locs}"
    )


URL = "http://downloads.openmicroscopy.org/bio-formats/{}/artifacts/loci_tools.jar"


def get_loci_tools() -> Path:
    """
    Finds the location of loci_tools.jar, if necessary download it to a
    writeable location.
    """
    for loc in _gen_jar_locations():
        if (loc / "loci_tools.jar").exists():
            return loc / "loci_tools.jar"

    logger.warn("loci_tools.jar not found, downloading")
    return download_jar()


def download_jar(version: str = "latest") -> Path:
    """Downloads the bioformats distribution of given version."""
    import hashlib

    dest = _get_writable_location() / "loci_tools.jar"

    url = URL.format(version)
    loci_tools = _download(url)
    with urllib.request.urlopen(url + ".sha1") as resp:
        checksum = resp.read().split(b" ")[0].decode()

    if hashlib.sha1(loci_tools).hexdigest() != checksum:
        raise IOError(
            "Downloaded loci_tools.jar has invalid checksum. Please try again."
        )
    dest.write_bytes(loci_tools)
    logger.warn("loci_tools.jar has been written to %s" % str(dest))
    return dest


def _download(url: str, progress: bool = True) -> bytes:
    with urllib.request.urlopen(url) as resp:
        total = resp.getheader("content-length")
        if total:
            total = int(total)
            block = max(4096, total // 40)
        else:
            block = 1000000

        if progress:
            print(f"downloading {url}")
        buffer = io.BytesIO()
        fetched = 0
        while True:
            chunk = resp.read(block)
            if not chunk:
                break
            buffer.write(chunk)
            fetched += len(chunk)
            if total and progress:
                print(f"progress: {(fetched / total) * 100:02.0f}%", end="\r")
    buffer.seek(0)
    return buffer.getvalue()


def _load_loci(
    java_mem: str = "1024m",
) -> "jpype.JPackage":
    import jpype

    loci_tools = get_loci_tools()
    if not jpype.isJVMStarted():
        jpype.startJVM(
            jpype.getDefaultJVMPath(),
            "-ea",
            f"-Djava.class.path={loci_tools}",
            "-Xmx" + java_mem,
            convertStrings=False,
        )
        log4j = jpype.JPackage("org.apache.log4j")
        log4j.BasicConfigurator.configure()
        log4j_logger = log4j.Logger.getRootLogger()
        log4j_logger.setLevel(log4j.Level.ERROR)

    return jpype.JPackage("loci")


def bioformats_xml(path: Union[str, Path]) -> str:
    """Return OME-XML for a file at `path` using bioformats reader."""
    loci = _load_loci()
    _meta = loci.formats.MetadataTools.createOMEXMLMetadata()
    rdr = loci.formats.ChannelSeparator(loci.formats.ChannelFiller())
    rdr.setMetadataStore(_meta)
    rdr.setId(str(path))
    return str(_meta.dumpXML())
