import os
import warnings
from typing import TYPE_CHECKING, Optional, Union

from .model import OME

try:
    from qtpy.QtCore import QMimeData, Qt
    from qtpy.QtWidgets import QTreeWidget, QTreeWidgetItem
except ImportError:
    raise ImportError(
        "qtpy and a Qt backend (pyside or pyqt) is required to use the OME widget:\n"
        "pip install qtpy pyqt5"
    )


if TYPE_CHECKING:
    import napari


class OMETree(QTreeWidget):
    """A Widget that can show OME XML"""

    def __init__(
        self, ome_dict: dict = None, viewer: "napari.viewer.Viewer" = None, parent=None
    ) -> None:
        super().__init__(parent=parent)
        if viewer is not None:
            viewer.layers.selection.events.active.connect(self._on_layer_change)
        self._viewer = viewer
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setIndentation(15)

        item = self.headerItem()
        font = item.font(0)
        font.setBold(True)
        item.setFont(0, font)
        self.clear()

        self._current_path: Optional[str] = None
        self.update(ome_dict)

    def clear(self):
        self.headerItem().setText(0, "drag/drop file...")
        super().clear()

    def _on_layer_change(self, event):
        layer = event.value
        if layer is not None:
            path = str(layer.source.path)
            if path.endswith((".tiff", ".tif")) and path != self._current_path:
                try:
                    ome = OME.from_tiff(path)
                except Exception:
                    return
                self._current_path = path
                self.update(ome)
                self.headerItem().setText(0, os.path.basename(path))
        else:
            self._current_path = None
            self.clear()

    def update(self, ome: Union[OME, str]):
        if not ome:
            return
        if isinstance(ome, OME):
            _ome = ome
        elif isinstance(ome, str):
            if ome == self._current_path:
                return
            try:
                if ome.endswith(".xml"):
                    _ome = OME.from_xml(ome)
                elif ome.lower().endswith((".tif", ".tiff")):
                    _ome = OME.from_tiff(ome)
                else:
                    warnings.warn(f"Unrecognized file type: {ome}")
                    return
            except Exception as e:
                warnings.warn(f"Could not parse OME metadata from {ome}: {e}")
                return
            self.headerItem().setText(0, os.path.basename(ome))
            self._current_path = ome
        else:
            raise TypeError("must be OME object or string")
        self._fill_item(_ome.dict(exclude_unset=True))

    def _fill_item(self, obj, item: QTreeWidgetItem = None):
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
        self, parent: QTreeWidgetItem, index: int, data: QMimeData, a
    ) -> bool:
        if data.hasUrls():
            for url in data.urls():
                lf = url.toLocalFile()
                if lf.endswith((".xml", ".tiff", ".tif")):
                    self.update(lf)
                    return True
        return False

    def mimeTypes(self):
        return ["text/uri-list"]

    def supportedDropActions(self):
        return Qt.CopyAction


if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication

    app = QApplication([])

    widget = OMETree()
    widget.show()

    app.exec()
