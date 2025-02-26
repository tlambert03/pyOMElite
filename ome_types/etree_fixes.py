from __future__ import annotations

from typing import TYPE_CHECKING

from ome_types._conversion import OME_2016_06_URI

if TYPE_CHECKING:
    from ome_types._conversion import AnyElementTree


NSMAP = {"": OME_2016_06_URI, "ome": OME_2016_06_URI}


# See note before using...
def fix_micro_manager_instrument(tree: AnyElementTree) -> AnyElementTree:
    """Fix MicroManager Instrument and Detector IDs and References.

    Some versions of OME-XML produced by MicroManager have invalid IDs (and references)
    for Instruments and Detectors. This function fixes those IDs and references.

    NOTE: as of v0.4.0, bad IDs and references are caught during ID validation anyway,
    so this is mostly an example of a fix function, and could be used to prevent
    the warning from being raised.
    """
    for i_idx, instrument in enumerate(tree.findall("Instrument", NSMAP)):
        old_id = instrument.get("ID")  # type: ignore [attr-defined]
        if old_id.startswith("Microscope"):
            new_id = f"Instrument:{i_idx}"
            instrument.set("ID", new_id)  # type: ignore [attr-defined]
            for ref in tree.findall(f".//InstrumentRef[@ID='{old_id}']", NSMAP):
                ref.set("ID", new_id)

        detectors = instrument.findall(".//Detector", NSMAP)  # type: ignore [attr-defined]
        for d_idx, detector in enumerate(detectors):
            old_id = detector.get("ID")
            if not old_id.startswith("Detector:"):
                new_id = f"Detector:{old_id if old_id.isdigit() else d_idx}"
                detector.set("ID", new_id)
                for ref in tree.findall(f".//DetectorSettings[@ID='{old_id}']", NSMAP):
                    ref.set("ID", new_id)

    return tree


ALL_FIXES = [fix_micro_manager_instrument]
__all__ = ["ALL_FIXES", "fix_micro_manager_instrument"]
