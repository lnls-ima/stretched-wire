# -*- coding: utf-8 -*-

from qtpy.QtWidgets import (
    QDialog as _QDialog,
    QVBoxLayout as _QVBoxLayout,
    )

from matplotlib.figure import Figure as _Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as _FigureCanvas,
    NavigationToolbar2QT as _Toolbar
    )

from stretchedwire.gui import utils as _utils

_font = _utils.get_default_font()
_font_bold = _utils.get_default_font(bold=True)
_icon_size = _utils.get_default_icon_size()


class PlotDialog(_QDialog):
    """Matplotlib plot dialog."""

    def __init__(self, parent=None):
        """Add figure canvas to layout."""
        super().__init__(parent)
        self.setFont(_font)
        self.figure = _Figure()
        self.canvas = _FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        _layout = _QVBoxLayout()
        _layout.addWidget(self.canvas)
        self.toolbar = _Toolbar(self.canvas, self)
        _layout.addWidget(self.toolbar)
        self.setLayout(_layout)

    def update_plot(self):
        """Update plot."""
        self.canvas.draw()

    def show(self):
        """Show dialog."""
        self.update_plot()
        super().show()
