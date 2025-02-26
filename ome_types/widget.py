from __future__ import annotations

import os
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ome_types.model import OME

try:
    from qtpy.QtCore import QMimeData, Qt
    from qtpy.QtWidgets import QTreeWidget, QTreeWidgetItem
except ImportError as e:
    raise ImportError(
        "qtpy and a Qt backend (pyside or pyqt) is required to use the OME widget:\n"
        "pip install qtpy pyqt5"
    ) from e


if TYPE_CHECKING:
    import napari.layers
    import napari.viewer
    from qtpy.QtWidgets import QWidget

METADATA_KEY = "ome_types"


class OMETree(QTreeWidget):
    """A Widget that can show OME XML."""

    def __init__(
        self,
        ome_meta: Path | OME | str | None | dict = None,
        viewer: napari.viewer.Viewer = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent=parent)
        self._viewer = viewer
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setIndentation(15)

        item = self.headerItem()
        font = item.font(0)
        font.setBold(True)
        item.setFont(0, font)
        self.clear()

        self._current_path: str | None = None
        if ome_meta:
            if isinstance(ome_meta, Path):
                ome_meta = str(ome_meta)
            self.update(ome_meta)

        if viewer is not None:
            viewer.layers.selection.events.active.connect(
                lambda e: self._try_load_layer(e.value)
            )
            self._try_load_layer(viewer.layers.selection.active)

    def clear(self) -> None:
        """Clear the widget and reset the header text."""
        self.headerItem().setText(0, "drag/drop file...")
        super().clear()

    def _try_load_layer(self, layer: napari.layers.Layer) -> None:
        """Handle napari viewer behavior."""
        if layer is not None:
            path = str(layer.source.path)

            # deprecated... don't do this ... it should be a dict
            if callable(layer.metadata):
                ome_meta = layer.metadata()
            elif isinstance(layer.metadata, OME):
                ome_meta = layer.metadata
            else:
                ome_meta = layer.metadata.get(METADATA_KEY)
                if callable(ome_meta):
                    ome_meta = ome_meta()

            ome = None
            if isinstance(ome_meta, OME):
                ome = ome_meta
            elif path.endswith((".tiff", ".tif")) and path != self._current_path:
                try:
                    ome = OME.from_tiff(path)
                except Exception:
                    return
            elif path.endswith(".nd2"):
                ome = self._try_from_nd2(path)
                if ome is None:
                    return
            if isinstance(ome, OME):
                self._current_path = path
                self.update(ome)
                self.headerItem().setText(0, os.path.basename(path))
        else:
            self._current_path = None
            self.clear()

    def _try_from_nd2(self, path: str) -> OME | None:
        try:
            import nd2

            with nd2.ND2File(path) as f:
                return f.ome_metadata()
        except Exception:
            return None

    def update(self, ome: OME | str | None | dict) -> None:
        """Update the widget with a new OME object or path to an OME XML file."""
        if not ome:
            return
        if isinstance(ome, OME):
            _ome = ome
        elif isinstance(ome, dict):
            _ome = OME(**ome)
        elif isinstance(ome, str):
            if ome == self._current_path:
                return
            try:
                if ome.endswith(".xml"):
                    _ome = OME.from_xml(ome)
                elif ome.lower().endswith((".tif", ".tiff")):
                    _ome = OME.from_tiff(ome)
                elif ome.lower().endswith(".nd2"):
                    _ome = self._try_from_nd2(ome)  # type: ignore
                    if _ome is None:
                        raise Exception()
                else:
                    warnings.warn(f"Unrecognized file type: {ome}", stacklevel=2)
                    return
            except Exception as e:
                warnings.warn(
                    f"Could not parse OME metadata from {ome}: {e}", stacklevel=2
                )
                return
            self.headerItem().setText(0, os.path.basename(ome))
            self._current_path = ome
        else:
            raise TypeError("must be OME object or string")
        data = _ome.model_dump(exclude_unset=True)
        self._fill_item(data)

    def _fill_item(self, obj: Any, item: QTreeWidgetItem = None) -> None:
        if item is None:
            self.clear()
            item = self.invisibleRootItem()
        if isinstance(obj, dict):
            for key, val in sorted(obj.items()):
                child = QTreeWidgetItem([key])
                item.addChild(child)
                self._fill_item(val, child)
        elif isinstance(obj, (list, tuple)):
            for n, val in enumerate(obj):
                text = val.get("id", n) if hasattr(val, "get") else n
                child = QTreeWidgetItem([str(text)])
                item.addChild(child)
                self._fill_item(val, child)
        else:
            t = getattr(obj, "value", str(obj))
            item.setText(0, f"{item.text(0)}: {t}")

    def dropMimeData(
        self, parent: QTreeWidgetItem, index: int, data: QMimeData, _: Any
    ) -> bool:
        """Handle drag/drop events to load OME XML files."""
        if data.hasUrls():
            for url in data.urls():
                lf = url.toLocalFile()
                if lf.endswith((".xml", ".tiff", ".tif", ".nd2")):
                    self.update(lf)
                    return True
        return False

    def mimeTypes(self) -> list[str]:
        """Return the supported mime types for drag/drop events."""
        return ["text/uri-list"]

    def supportedDropActions(self) -> Qt.DropActions:
        """Return the supported drop actions for drag/drop events."""
        return Qt.CopyAction


if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication

    app = QApplication([])

    widget = OMETree()
    widget.show()

    app.exec()
